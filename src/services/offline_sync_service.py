"""Offline synchronization service for buffering and syncing local records."""

from datetime import datetime
import json
from typing import Any, Dict, List
from src.database.connection import db_connection
from src.logger import logger


class OfflineSyncService:
    """Manages offline transaction queues and synchronization state."""

    @staticmethod
    async def queue_operation(
        operation_type: str,
        table_name: str,
        payload: Dict[str, Any],
    ) -> bool:
        """Buffers an insert/update/delete operation when running offline."""
        query = """
            INSERT INTO sync_queue (operation, target_table, payload, status, created_at)
            VALUES (?, ?, ?, 'PENDING', ?)
        """
        try:
            async with db_connection.get_db() as db:
                await db.execute(
                    query,
                    (
                        operation_type.upper(),
                        table_name,
                        json.dumps(payload),
                        datetime.now().isoformat(),
                    ),
                )
                await db.commit()
            logger.info(f"Queued offline operation '{operation_type}' on table '{table_name}'")
            return True
        except Exception as ex:
            logger.error(f"Failed to queue sync operation: {str(ex)}")
            return False

    @staticmethod
    async def get_pending_sync_items() -> List[Dict[str, Any]]:
        """Fetches all operations awaiting cloud synchronization."""
        query = """
            SELECT id, operation, target_table, payload, created_at
            FROM sync_queue
            WHERE status = 'PENDING'
            ORDER BY id ASC
        """
        async with db_connection.get_db() as db:
            cursor = await db.execute(query)
            rows = await cursor.fetchall()
            return [
                {
                    "id": row[0],
                    "operation": row[1],
                    "target_table": row[2],
                    "payload": json.loads(row[3]),
                    "created_at": row[4],
                }
                for row in rows
            ]

    @staticmethod
    async def mark_synced(sync_id: int) -> bool:
        """Marks a buffered operation as successfully synced."""
        query = """
            UPDATE sync_queue
            SET status = 'SYNCED', synced_at = ?
            WHERE id = ?
        """
        try:
            async with db_connection.get_db() as db:
                await db.execute(query, (datetime.now().isoformat(), sync_id))
                await db.commit()
            return True
        except Exception as ex:
            logger.error(f"Failed to update sync item status {sync_id}: {str(ex)}")
            return False
