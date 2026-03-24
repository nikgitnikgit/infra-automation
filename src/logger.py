"""
logger.py - Centralized logging configuration for infra-automation.
"""

import logging
import os
import re


LOG_FILE = os.path.join(os.path.dirname(__file__), "..", "logs", "provisioning.log")

# Strip ANSI escape codes from log messages
ANSI_ESCAPE = re.compile(r'\x1B(?:[@-Z\\-_]|\[[0-?]*[ -/]*[@-~])')


class CleanFormatter(logging.Formatter):
    """Formatter that strips ANSI escape codes before writing to file."""
    def format(self, record):
        record.msg = ANSI_ESCAPE.sub('', str(record.msg))
        return super().format(record)


def setup_logging(log_file: str = LOG_FILE) -> logging.Logger:
    """
    Configure and return a logger that writes to both file and stdout.
    File handler strips ANSI codes. Console handler shows them as-is.
    """
    os.makedirs(os.path.dirname(log_file), exist_ok=True)

    logger = logging.getLogger("infra-automation")
    logger.setLevel(logging.DEBUG)

    if logger.handlers:
        return logger

    formatter = logging.Formatter(
        "%(asctime)s  [%(levelname)-8s]  %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )

    clean_formatter = CleanFormatter(
        "%(asctime)s  [%(levelname)-8s]  %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )

    # File handler — clean, no ANSI codes
    fh = logging.FileHandler(log_file)
    fh.setLevel(logging.DEBUG)
    fh.setFormatter(clean_formatter)

    # Console handler — normal output
    ch = logging.StreamHandler()
    ch.setLevel(logging.INFO)
    ch.setFormatter(formatter)

    logger.addHandler(fh)
    logger.addHandler(ch)

    return logger


logger = setup_logging()
