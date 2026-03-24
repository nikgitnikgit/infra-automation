"""
input_handler.py - Collect VM definitions from the user interactively,
validate them, and persist to configs/instances.json.
"""

import json
import os
from src.validator import validate_instance_input, VALID_OS
from src.logger import logger

CONFIGS_DIR = os.path.join(os.path.dirname(__file__), "..", "configs")
INSTANCES_FILE = os.path.join(CONFIGS_DIR, "instances.json")

STOP_WORDS = {"done", "finish", "stop"}
VALID_SERVICES = {"nginx", "mysql"}


def _prompt_int(prompt: str, min_val: int, max_val: int) -> int:
    """Keep asking until the user enters an integer in [min_val, max_val]."""
    while True:
        raw = input(prompt).strip()
        try:
            value = int(raw)
            if min_val <= value <= max_val:
                return value
            print(f"  ✗  Please enter a number between {min_val} and {max_val}.")
        except ValueError:
            print("  ✗  That's not a valid integer.")


def _prompt_os(prompt: str) -> str:
    """Keep asking until the user enters a valid OS from VALID_OS."""
    while True:
        raw = input(prompt).strip().lower()
        if raw in VALID_OS:
            return raw.title()
        print(f"  ✗  '{raw}' is not supported. Choose from: {', '.join(sorted(VALID_OS))}")


def _prompt_services(prompt: str) -> list:
    """Keep asking until the user enters valid services or leaves blank."""
    services_hint = ", ".join(sorted(VALID_SERVICES))
    while True:
        raw = input(prompt).strip()
        if not raw:
            return []
        services = [s.strip().lower() for s in raw.split(",") if s.strip()]
        invalid = [s for s in services if s not in VALID_SERVICES]
        if invalid:
            print(f"  ✗  Invalid service(s): {', '.join(invalid)}. Choose from: {services_hint}")
        else:
            return services


def get_user_input() -> list[dict]:
    """
    Interactively prompt the user for one or more VM definitions.
    Saves to JSON after each machine is successfully added.
    Returns a list of validated machine config dicts.
    """
    machines = []
    existing_names = set()
    os_options = ", ".join(sorted(VALID_OS))
    services_options = ", ".join(sorted(VALID_SERVICES))
    stop_hint = "/".join(sorted(STOP_WORDS))

    print(f"\nSupported operating systems: {os_options}")
    print(f"Supported services: {services_options}")
    print(f"Type '{stop_hint}' as the machine name when finished.\n")

    while True:
        name = input(f"Machine name (or '{stop_hint}' to finish): ").strip()

        # Check stop words
        if name.lower() in STOP_WORDS:
            if not machines:
                print("  !  No machines defined. Exiting.")
            break

        # Check empty name
        if not name:
            print("  ✗  Machine name cannot be empty. Please enter a valid name.")
            continue

        # Check duplicate name
        if name.lower() in existing_names:
            print(f"  ✗  A machine named '{name}' already exists. Please use a different name.")
            continue

        os_choice = _prompt_os(f"  OS [{os_options}]: ")
        cpu = _prompt_int("  vCPUs (1-64): ", 1, 64)
        ram = _prompt_int("  RAM in GB (1-512): ", 1, 512)
        services = _prompt_services(
            f"  Services to install ({services_options}) or leave blank: "
        )

        raw = {"name": name, "os": os_choice, "cpu": cpu, "ram": ram, "services": services}

        try:
            validated = validate_instance_input(raw)
            machines.append(validated)
            existing_names.add(name.lower())
            # Save immediately after each successful machine addition
            save_instances(machines)
            print(f"  ✓  Machine '{validated['name']}' added and saved.\n")
            logger.info(f"User defined machine: {validated}")
        except ValueError as exc:
            print(f"  ✗  Validation error: {exc}\n  Please try again.\n")

    return machines


def save_instances(machines: list[dict], path: str = INSTANCES_FILE) -> None:
    """Persist the validated machine list to a JSON file."""
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w") as fh:
        json.dump(machines, fh, indent=4)
    logger.info(f"Saved {len(machines)} machine(s) to {path}")


def load_instances(path: str = INSTANCES_FILE) -> list[dict]:
    """Load previously saved machine configs from JSON."""
    if not os.path.isfile(path):
        logger.warning(f"Instances file not found: {path}")
        return []
    with open(path) as fh:
        data = json.load(fh)
    logger.info(f"Loaded {len(data)} machine(s) from {path}")
    return data
