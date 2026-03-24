"""
validator.py - Input validation for machine configurations using pydantic.
Falls back to manual validation if pydantic is not installed.
"""

import re
from typing import Any

try:
    from pydantic import BaseModel, field_validator, ValidationError
    PYDANTIC_AVAILABLE = True
except ImportError:
    PYDANTIC_AVAILABLE = False

from src.logger import logger

# -----------------------------------------------------------------------
# Allowed values
# -----------------------------------------------------------------------
VALID_OS = {"ubuntu", "centos", "debian", "fedora", "amazon linux"}
MIN_CPU, MAX_CPU = 1, 64
MIN_RAM, MAX_RAM = 1, 512   # GB


# -----------------------------------------------------------------------
# Pydantic schema (preferred)
# -----------------------------------------------------------------------
if PYDANTIC_AVAILABLE:
    class MachineSchema(BaseModel):
        name: str
        os: str
        cpu: int
        ram: int
        services: list = []

        @field_validator("name")
        @classmethod
        def name_must_be_valid(cls, v: str) -> str:
            v = v.strip()
            if not re.match(r"^[a-zA-Z0-9][a-zA-Z0-9\-_]{1,62}$", v):
                raise ValueError(
                    "Machine name must be 2-63 chars, alphanumeric/hyphens/underscores, "
                    "and start with a letter or digit."
                )
            return v

        @field_validator("os")
        @classmethod
        def os_must_be_supported(cls, v: str) -> str:
            if v.strip().lower() not in VALID_OS:
                raise ValueError(
                    f"OS '{v}' is not supported. Choose from: {', '.join(sorted(VALID_OS))}"
                )
            return v.strip().lower().title()

        @field_validator("cpu")
        @classmethod
        def cpu_in_range(cls, v: int) -> int:
            if not (MIN_CPU <= v <= MAX_CPU):
                raise ValueError(f"CPU must be between {MIN_CPU} and {MAX_CPU} vCPUs.")
            return v

        @field_validator("ram")
        @classmethod
        def ram_in_range(cls, v: int) -> int:
            if not (MIN_RAM <= v <= MAX_RAM):
                raise ValueError(f"RAM must be between {MIN_RAM} and {MAX_RAM} GB.")
            return v


# -----------------------------------------------------------------------
# Public validation function
# -----------------------------------------------------------------------

def validate_instance_input(data: dict) -> dict:
    """
    Validate a raw machine-config dictionary.
    Returns the cleaned/normalised dict on success.
    Raises ValueError with a descriptive message on failure.
    """
    if PYDANTIC_AVAILABLE:
        try:
            validated = MachineSchema(**data)
            return validated.model_dump()
        except ValidationError as exc:
            errors = "; ".join(e["msg"] for e in exc.errors())
            logger.error(f"Validation failed for {data.get('name', '?')}: {errors}")
            raise ValueError(errors) from exc
    else:
        # Manual fallback
        errors = []
        name = str(data.get("name", "")).strip()
        if not re.match(r"^[a-zA-Z0-9][a-zA-Z0-9\-_]{1,62}$", name):
            errors.append("Invalid machine name.")

        os_val = str(data.get("os", "")).strip().lower()
        if os_val not in VALID_OS:
            errors.append(f"Unsupported OS '{os_val}'.")

        try:
            cpu = int(data.get("cpu", 0))
            if not (MIN_CPU <= cpu <= MAX_CPU):
                errors.append(f"CPU must be {MIN_CPU}–{MAX_CPU}.")
        except (TypeError, ValueError):
            errors.append("CPU must be an integer.")

        try:
            ram = int(data.get("ram", 0))
            if not (MIN_RAM <= ram <= MAX_RAM):
                errors.append(f"RAM must be {MIN_RAM}–{MAX_RAM} GB.")
        except (TypeError, ValueError):
            errors.append("RAM must be an integer.")

        if errors:
            msg = "; ".join(errors)
            logger.error(f"Validation failed for '{name}': {msg}")
            raise ValueError(msg)

        return {
            "name": name,
            "os": os_val.title(),
            "cpu": int(data["cpu"]),
            "ram": int(data["ram"]),
            "services": data.get("services", []),
        }
