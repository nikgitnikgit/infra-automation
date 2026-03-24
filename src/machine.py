"""
machine.py - Machine class representing a virtual machine configuration.
"""

from dataclasses import dataclass, field, asdict
from typing import Optional
from src.logger import logger


SUPPORTED_OS = {"ubuntu", "centos", "debian", "fedora", "amazon linux"}


@dataclass
class Machine:
    """
    Represents a virtual machine with its provisioning configuration.
    """
    name: str
    os: str
    cpu: int          # number of vCPUs
    ram: int          # RAM in GB
    services: list = field(default_factory=list)

    def __post_init__(self):
        """Normalise fields and log creation."""
        self.name = self.name.strip()
        self.os = self.os.strip().lower().title()
        logger.info(f"Machine object created: {self.name} ({self.os}, {self.cpu} vCPU, {self.ram} GB RAM)")

    # ------------------------------------------------------------------
    # Representation helpers
    # ------------------------------------------------------------------

    def to_dict(self) -> dict:
        """Return a plain dictionary representation of the machine."""
        return asdict(self)

    def __str__(self) -> str:
        services_str = ", ".join(self.services) if self.services else "none"
        return (
            f"Machine(name={self.name!r}, os={self.os!r}, "
            f"cpu={self.cpu} vCPU, ram={self.ram} GB, services=[{services_str}])"
        )

    # ------------------------------------------------------------------
    # Provisioning helpers
    # ------------------------------------------------------------------

    def add_service(self, service: str) -> None:
        """Register a service to be installed on this machine."""
        service = service.strip().lower()
        if service not in self.services:
            self.services.append(service)
            logger.info(f"Service '{service}' added to machine '{self.name}'.")

    def log_creation(self) -> None:
        """Log a human-readable provisioning summary."""
        logger.info(f"Provisioning summary — {self}")
