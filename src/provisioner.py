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
        logger.error(f"[{machine_name}] Script not found: {script_path}")
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
        logger.info(f"[{machine_name}] Script completed successfully: {os.path.basename(script_path)}")
        return True
    except subprocess.CalledProcessError as exc:
        logger.error(f"[{machine_name}] Script failed (exit {exc.returncode}): {os.path.basename(script_path)}")
        for line in (exc.stderr or "").splitlines():
            logger.error(f"[{machine_name}] STDERR: {line}")
        return False
    except FileNotFoundError:
        logger.error(f"[{machine_name}] 'bash' not found. Is Git Bash installed and in PATH?")
        return False
    except Exception as exc:
        logger.error(f"[{machine_name}] Unexpected error running script: {exc}")
        return False


def provision_machine(machine) -> bool:
    """
    Mock-provision a Machine object.
    Runs the base setup script, then any service-specific scripts.
    Returns True if all steps succeed.
    """
    logger.info(f"{'='*50}")
    logger.info(f"Provisioning started: {machine.name}")
    logger.info(f"  OS: {machine.os} | CPU: {machine.cpu} vCPU | RAM: {machine.ram} GB")
    logger.info(f"  Services: {', '.join(machine.services) if machine.services else 'none'}")
    logger.info(f"{'='*50}")

    try:
        # --- Step 1: base setup ---
        base_script = os.path.join(SCRIPTS_DIR, "setup_base.sh")
        if not _run_script(base_script, machine.name):
            logger.error(f"[{machine.name}] Base setup FAILED. Aborting provisioning.")
            return False

        # --- Step 2: per-service scripts ---
        for service in machine.services:
            script = os.path.join(SCRIPTS_DIR, f"setup_{service}.sh")
            if not _run_script(script, machine.name):
                logger.error(f"[{machine.name}] Service '{service}' setup FAILED.")
                return False
            logger.info(f"[{machine.name}] Service '{service}' installed successfully.")

        # --- Step 3: mock delay ---
        logger.info(f"[{machine.name}] Finalizing provisioning...")
        time.sleep(1)

        logger.info(f"{'='*50}")
        logger.info(f"Provisioning COMPLETED successfully: {machine.name}")
        logger.info(f"{'='*50}")
        return True

    except Exception as exc:
        logger.error(f"[{machine.name}] Unexpected error during provisioning: {exc}")
        return False
