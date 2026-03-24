#!/usr/bin/env python3
"""
infra_simulator.py - Entry point for the Infrastructure Provisioning Simulator.

Usage:
    python infra_simulator.py          # interactive mode (prompts for input)
    python infra_simulator.py --load   # re-provision from configs/instances.json
"""

import argparse
import sys
import os

# Make sure src/ is importable when running from the project root
sys.path.insert(0, os.path.dirname(__file__))

from src.logger import logger
from src.machine import Machine
from src.input_handler import get_user_input, save_instances, load_instances
from src.provisioner import provision_machine


def build_machines(configs: list[dict]) -> list[Machine]:
    """Convert raw config dicts into Machine objects."""
    machines = []
    for cfg in configs:
        m = Machine(
            name=cfg["name"],
            os=cfg["os"],
            cpu=cfg["cpu"],
            ram=cfg["ram"],
            services=cfg.get("services", []),
        )
        machines.append(m)
    return machines


def run(load_existing: bool = False) -> None:
    logger.info("=" * 60)
    logger.info("Infrastructure Provisioning Simulator — START")
    logger.info("=" * 60)

    if load_existing:
        configs = load_instances()
        if not configs:
            logger.error("No saved instances found. Run without --load to define new machines.")
            sys.exit(1)
        print(f"\nLoaded {len(configs)} machine(s) from configs/instances.json.\n")
    else:
        configs = get_user_input()
        save_instances(configs)

    machines = build_machines(configs)

    success_count = 0
    fail_count = 0

    for machine in machines:
        ok = provision_machine(machine)
        if ok:
            success_count += 1
        else:
            fail_count += 1

    logger.info("=" * 60)
    logger.info(
        f"Provisioning finished — "
        f"{success_count} succeeded, {fail_count} failed."
    )
    logger.info("=" * 60)

    if fail_count:
        sys.exit(1)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Infrastructure Provisioning Simulator")
    parser.add_argument(
        "--load",
        action="store_true",
        help="Skip interactive input and re-provision from configs/instances.json",
    )
    args = parser.parse_args()
    run(load_existing=args.load)
