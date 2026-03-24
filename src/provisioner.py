"""
provisioner.py - Simulates (mocked) infrastructure provisioning.
Executes Bash setup scripts via subprocess.
"""

import subprocess
import os
import time
from src.logger import logger

SCRIPTS_DIR = os.path.join(os.path.dirname(__file__), "..", "scripts")


def _run_script(script_path: str, machine_name: str) -> bool:
    """
    Execute a Bash script and return True on success.
    """
    if not os.path.isfile(script_path):
        logger.error(f"Script not found: {script_path}")
        return False

    logger.info(f"[{machine_name}] Running script: {script_path}")
    try:
        result = subprocess.run(
            ["bash", script_path, machine_name],
            check=True,
            capture_output=True,
            text=True,
        )
        for line in result.stdout.splitlines():
            logger.info(f"[{machine_name}] {line}")
        return True
    except subprocess.CalledProcessError as exc:
        logger.error(f"[{machine_name}] Script failed (exit {exc.returncode}).")
        for line in (exc.stderr or "").splitlines():
            logger.error(f"[{machine_name}] STDERR: {line}")
        return False


def provision_machine(machine) -> bool:
    """
    Mock-provision a Machine object.
    Runs the base setup script, then any service-specific scripts.
    Returns True if all steps succeed.
    """
    logger.info(f"=== Provisioning started: {machine.name} ===")
    machine.log_creation()

    # --- Step 1: base setup ---
    base_script = os.path.join(SCRIPTS_DIR, "setup_base.sh")
    if not _run_script(base_script, machine.name):
        logger.error(f"Base setup failed for {machine.name}. Aborting.")
        return False

    # --- Step 2: per-service scripts ---
    for service in machine.services:
        script = os.path.join(SCRIPTS_DIR, f"setup_{service}.sh")
        if not _run_script(script, machine.name):
            logger.error(f"Service setup failed for '{service}' on {machine.name}.")
            return False

    # --- Step 3: mock delay to simulate real provisioning ---
    logger.info(f"[{machine.name}] Simulating provisioning delay…")
    time.sleep(1)

    logger.info(f"=== Provisioning complete: {machine.name} ===")
    return True
