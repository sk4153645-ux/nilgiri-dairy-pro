"""Application entry point and desktop launcher."""

import asyncio
import os
import sys

# Ensure project root is available in sys.path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from src.database.migration import run_migrations
from src.logger import logger


def bootstrap():
    """Initializes database schema and bootstraps Kivy UI."""
    try:
        logger.info("Initializing Nilgiri Dairy Pro system...")
        
        # Run pending database migrations
        asyncio.run(run_migrations())
        logger.info("Database migrations completed successfully.")

        # Launch Main Application Window
        from src.main import NilgiriDairyApp
        NilgiriDairyApp().run()

    except KeyboardInterrupt:
        logger.warning("Application interrupted by user.")
        sys.exit(0)
    except Exception as ex:
        logger.critical(f"Fatal error during application launch: {str(ex)}", exc_info=True)
        sys.exit(1)


if __name__ == "__main__":
    bootstrap()
