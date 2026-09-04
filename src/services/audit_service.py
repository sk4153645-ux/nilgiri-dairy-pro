"""Audit service to track and log system-wide data mutations."""

from datetime import datetime
import json
from typing import Any, Dict, List, Optional
from src.database.connection import db_connection
from src.logger import logger


class AuditService:
    """Handles persistent logging of changes to farmers, milk entries, and accounts."""

    @staticmethod
    async def log_action(
        user_id: int,
        action: str,
        entity_name: str,
        entity_id: Optional[int] = None,
        details: Optional[Dict[str, Any]] = None,
    ) -> bool:
        """Records an action in the audit logs table."""
        try:
            query = """
                INSERT INTO audit_logs (user_id, action, entity_name, entity_id, details, timestamp)
                VALUES (?, ?, ?, ?, ?, ?)
            """
            serialized_details = json.dumps(details) if details else "{}"
            now = datetime.now().isoformat()

            async with db_connection.get_db() as db:
                await db.execute(
                    query,
                    (user_id, action, entity_name, entity_id, serialized_details, now),
                )
                await db.commit()

            logger.info(f"Audit log recorded: {action} on {entity_name} (ID: {entity_id}) by User {user_id}")
            return True
        except Exception as ex:
            logger.error(f"Failed to record audit log: {str(ex)}")
            return False

    @staticmethod
    async def get_logs_for_entity(entity_name: str, entity_id: int) -> List[Dict[str, Any]]:
        """Retrieves audit trail for a specific entity."""
        query = """
            SELECT id, user_id, action, entity_name, entity_id, details, timestamp
            FROM audit_logs
            WHERE entity_name = ? AND entity_id = ?
            ORDER BY id DESC
        """
        async with db_connection.get_db() as db:
            cursor = await db.execute(query, (entity_name, entity_id))
            rows = await cursor.fetchall()
            return [
                {
                    "id": row[0],
                    "user_id": row[1],
                    "action": row[2],
                    "entity_name": row[3],
                    "entity_id": row[4],
                    "details": json.loads(row[5]) if row[5] else {},
                    "timestamp": row[6],
                }
                for row in rows
            ]
