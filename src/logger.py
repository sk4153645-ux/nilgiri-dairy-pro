"""Application logging configuration using Loguru."""

import os
import sys
from pathlib import Path
from loguru import logger


def setup_logger():
    """Configure loguru sinks safely for packaged windowed builds."""
    logger.remove()

    # Check if stderr exists and is not None
    if getattr(sys, "stderr", None) is not None:
        try:
            logger.add(
                sys.stderr,
                format="<green>{time:YYYY-MM-DD HH:mm:ss}</green> | <level>{level: <8}</level> | <cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - <level>{message}</level>",
                level="INFO",
            )
        except Exception:
            pass

    # File logging
    log_dir = Path(os.environ.get("APPDATA", Path.home())) / "NilgiriDairyPro" / "logs"
    try:
        log_dir.mkdir(parents=True, exist_ok=True)
        log_file = log_dir / "app.log"
        logger.add(
            str(log_file),
            rotation="10 MB",
            retention="7 days",
            level="DEBUG",
            encoding="utf-8",
        )
    except Exception:
        pass

    return logger


setup_logger()
