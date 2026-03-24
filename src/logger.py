"""
logger.py - Centralized logging configuration for infra-automation.
"""

import logging
import os

LOG_FILE = os.path.join(os.path.dirname(__file__), "..", "logs", "provisioning.log")


def setup_logging(log_file: str = LOG_FILE) -> logging.Logger:
    """
    Configure and return a logger that writes to both file and stdout.
    """
    os.makedirs(os.path.dirname(log_file), exist_ok=True)

    logger = logging.getLogger("infra-automation")
    logger.setLevel(logging.DEBUG)

    # Avoid duplicate handlers if setup_logging is called more than once
    if logger.handlers:
        return logger

    formatter = logging.Formatter(
        "%(asctime)s  [%(levelname)-8s]  %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )

    # File handler
    fh = logging.FileHandler(log_file)
    fh.setLevel(logging.DEBUG)
    fh.setFormatter(formatter)

    # Console handler
    ch = logging.StreamHandler()
    ch.setLevel(logging.INFO)
    ch.setFormatter(formatter)

    logger.addHandler(fh)
    logger.addHandler(ch)

    return logger


# Module-level logger instance — import this everywhere
logger = setup_logging()
