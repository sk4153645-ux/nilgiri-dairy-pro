"""Application-wide logger configuration using loguru."""

import os
import sys
from loguru import logger

# Create logs directory if it doesn't exist
LOGS_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "logs")
os.makedirs(LOGS_DIR, exist_ok=True)


def setup_logger(log_file: str = "app.log", rotation: str = "10 MB", retention: str = "30 days"):
    """Configures handlers for logging."""
    logger.remove()

    # Console logging
    logger.add(
        sys.stdout,
        format="<green>{time:YYYY-MM-DD HH:mm:ss}</green> | <level>{level: <8}</level> | <cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - <level>{message}</level>",
        level="INFO",
    )

    # File logging
    log_path = os.path.join(LOGS_DIR, log_file)
    logger.add(
        log_path,
        rotation=rotation,
        retention=retention,
        compression="zip",
        level="DEBUG",
        encoding="utf-8",
    )
    return logger


# Default logger instance
setup_logger()

__all__ = ["logger", "setup_logger"]
