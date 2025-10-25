"""Logging configuration helpers."""

from __future__ import annotations

import logging
from typing import Optional


def get_logger(name: str, log_file: Optional[str] = None) -> logging.Logger:
    """Return a logger configured for console (and optional file) output."""

    logger = logging.getLogger(name)
    if logger.handlers:
        return logger

    logger.setLevel(logging.INFO)
    formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")

    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)

    if log_file:
        file_handler = logging.FileHandler(log_file)
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)

    return logger
