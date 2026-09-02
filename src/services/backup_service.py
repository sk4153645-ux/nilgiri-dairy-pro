"""
Backup Service

Handles database backup and restore operations.
"""

import shutil
from pathlib import Path
from datetime import datetime
from typing import Tuple
from src.config import Config
from src.logger import setup_logger

logger = setup_logger(__name__)


class BackupService:
    """
    Database backup and restore service.

    Features:
        - Automatic backups
        - Manual backup on demand
        - Restore from backup
        - Backup cleanup
    """

    @staticmethod
    def create_backup() -> Tuple[bool, str, str]:
        """
        Create database backup.

        Returns:
            Tuple of (success, message, backup_path)
        """
        try:
            if not Config.ENABLE_BACKUP:
                return False, "Backup disabled", ""

            # Create backup directory
            backup_dir = Path(Config.BACKUP_PATH)
            backup_dir.mkdir(parents=True, exist_ok=True)

            # Create backup filename with timestamp
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            backup_file = backup_dir / f"dairy_backup_{timestamp}.db"

            # Copy database file
            db_path = Path(Config.DATABASE_PATH)
            if db_path.exists():
                shutil.copy2(db_path, backup_file)
                logger.info(f"Backup created: {backup_file}")
                return True, f"Backup created: {backup_file.name}", str(backup_file)
            else:
                return False, "Database file not found", ""
        except Exception as e:
            logger.error(f"Backup failed: {e}")
            return False, f"Backup failed: {str(e)}", ""

    @staticmethod
    def restore_backup(backup_path: str) -> Tuple[bool, str]:
        """
        Restore from backup.

        Args:
            backup_path: Path to backup file

        Returns:
            Tuple of (success, message)
        """
        try:
            backup_file = Path(backup_path)
            if not backup_file.exists():
                return False, "Backup file not found"

            # Create restore timestamp
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            db_path = Path(Config.DATABASE_PATH)
            current_backup = db_path.parent / f"dairy_current_{timestamp}.db"

            # Backup current database
            if db_path.exists():
                shutil.copy2(db_path, current_backup)

            # Restore from backup
            shutil.copy2(backup_file, db_path)
            logger.info(f"Restored from backup: {backup_path}")
            return True, "Restored successfully"
        except Exception as e:
            logger.error(f"Restore failed: {e}")
            return False, f"Restore failed: {str(e)}"

    @staticmethod
    def list_backups() -> Tuple[bool, str, list]:
        """
        List all available backups.

        Returns:
            Tuple of (success, message, backups_list)
        """
        try:
            backup_dir = Path(Config.BACKUP_PATH)
            if not backup_dir.exists():
                return True, "No backups found", []

            backups = sorted(
                backup_dir.glob("dairy_backup_*.db"),
                key=lambda x: x.stat().st_mtime,
                reverse=True,
            )

            backup_list = [
                {
                    "filename": b.name,
                    "path": str(b),
                    "size": b.stat().st_size,
                    "created": datetime.fromtimestamp(b.stat().st_mtime).isoformat(),
                }
                for b in backups
            ]

            return True, f"Found {len(backup_list)} backups", backup_list
        except Exception as e:
            logger.error(f"Failed to list backups: {e}")
            return False, "Failed to list backups", []
