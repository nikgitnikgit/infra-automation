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


def get_user_input() -> list[dict]:
    """
    Interactively prompt the user for one or more VM definitions.
    Returns a list of validated machine config dicts.
    """
    machines = []
    os_options = ", ".join(sorted(VALID_OS))
    stop_hint = "/".join(sorted(STOP_WORDS))
    print(f"\nSupported operating systems: {os_options}")
    print(f"Type '{stop_hint}' as the machine name when finished.\n")

    while True:
        name = input(f"Machine name (or '{stop_hint}' to finish): ").strip()
        if name.lower() in STOP_WORDS:
            if not machines:
                print("  ✗  You must define at least one machine.")
                continue
            break

        os_choice = _prompt_os(f"  OS [{os_options}]: ")
        cpu = _prompt_int("  vCPUs (1-64): ", 1, 64)
        ram = _prompt_int("  RAM in GB (1-512): ", 1, 512)

        services_raw = input("  Services to install (comma-separated, e.g. nginx,mysql) or leave blank: ").strip()
        services = [s.strip().lower() for s in services_raw.split(",") if s.strip()]

        raw = {"name": name, "os": os_choice, "cpu": cpu, "ram": ram, "services": services}

        try:
            validated = validate_instance_input(raw)
            machines.append(validated)
            print(f"  ✓  Machine '{validated['name']}' added.\n")
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
