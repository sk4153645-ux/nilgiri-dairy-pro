"""
Database Connection Management

Provides connection pooling, context managers, and thread-safe database access.
Uses SQLite with proper error handling and logging.
"""

import sqlite3
import threading
from contextlib import contextmanager
from typing import Optional, List, Dict, Any
from src.config import Config
from src.logger import setup_logger
from src.core.exceptions import DatabaseError

logger = setup_logger(__name__)


class DatabaseConnection:
    """
    Thread-safe database connection manager with connection pooling.

    Features:
        - Connection pooling
        - Thread-safe operations
        - Automatic error handling
        - Connection retry logic
        - Query logging
    """

    def __init__(self, db_path: str = None):
        """
        Initialize database connection.

        Args:
            db_path: Path to SQLite database file
        """
        self.db_path = db_path or Config.DATABASE_PATH
        self.pool: List[sqlite3.Connection] = []
        self.pool_lock = threading.Lock()
        self.pool_size = Config.DB_POOL_SIZE
        self.timeout = Config.DB_TIMEOUT
        self._initialize_pool()

    def _initialize_pool(self) -> None:
        """
        Initialize connection pool.

        Creates initial connections in the pool.
        """
        try:
            for _ in range(self.pool_size):
                conn = sqlite3.connect(
                    self.db_path,
                    timeout=self.timeout,
                    check_same_thread=False,
                )
                conn.row_factory = sqlite3.Row  # Return rows as dictionaries
                conn.execute("PRAGMA journal_mode = WAL")  # Write-Ahead Logging
                conn.execute("PRAGMA foreign_keys = ON")  # Enable foreign keys
                self.pool.append(conn)
            logger.info(f"Database connection pool initialized with {self.pool_size} connections")
        except sqlite3.Error as e:
            logger.error(f"Failed to initialize database connection pool: {e}")
            raise DatabaseError(
                f"Failed to initialize database: {str(e)}",
                details={"db_path": self.db_path},
            )

    @contextmanager
    def get_connection(self) -> sqlite3.Connection:
        """
        Get a database connection from the pool.

        Yields:
            SQLite connection object

        Example:
            >>> with db.get_connection() as conn:
            ...     cursor = conn.cursor()
            ...     cursor.execute("SELECT * FROM farmers")

        Raises:
            DatabaseError: If unable to get connection
        """
        conn = None
        try:
            with self.pool_lock:
                if not self.pool:
                    # Create new connection if pool is empty
                    conn = sqlite3.connect(
                        self.db_path,
                        timeout=self.timeout,
                        check_same_thread=False,
                    )
                    conn.row_factory = sqlite3.Row
                else:
                    conn = self.pool.pop()

            yield conn
        except sqlite3.Error as e:
            logger.error(f"Database connection error: {e}")
            raise DatabaseError(f"Database error: {str(e)}")
        finally:
            if conn:
                with self.pool_lock:
                    if len(self.pool) < self.pool_size:
                        self.pool.append(conn)
                    else:
                        conn.close()

    def execute_query(
        self, query: str, params: tuple = (), fetch_one: bool = False
    ) -> Any:
        """
        Execute SELECT query.

        Args:
            query: SQL query string
            params: Query parameters for safe execution
            fetch_one: If True, return single row; else return all rows

        Returns:
            Query result (single row dict, list of row dicts, or None)

        Raises:
            DatabaseError: If query execution fails
        """
        try:
            with self.get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute(query, params)
                logger.debug(f"Query executed: {query} with params: {params}")

                if fetch_one:
                    return cursor.fetchone()
                return cursor.fetchall()
        except sqlite3.Error as e:
            logger.error(f"Query execution failed: {e}\nQuery: {query}")
            raise DatabaseError(
                f"Query execution failed: {str(e)}",
                query=query,
                details={"params": params},
            )

    def execute_update(
        self, query: str, params: tuple = ()
    ) -> int:
        """
        Execute INSERT/UPDATE/DELETE query.

        Args:
            query: SQL query string
            params: Query parameters for safe execution

        Returns:
            Number of affected rows

        Raises:
            DatabaseError: If query execution fails
        """
        try:
            with self.get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute(query, params)
                conn.commit()
                affected = cursor.rowcount
                logger.info(f"Update query executed: {affected} rows affected")
                return affected
        except sqlite3.Error as e:
            logger.error(f"Update execution failed: {e}\nQuery: {query}")
            raise DatabaseError(
                f"Update execution failed: {str(e)}",
                query=query,
                details={"params": params},
            )

    def execute_insert(
        self, query: str, params: tuple = ()
    ) -> int:
        """
        Execute INSERT query and return last inserted ID.

        Args:
            query: SQL INSERT query
            params: Query parameters

        Returns:
            Last inserted row ID

        Raises:
            DatabaseError: If insert fails
        """
        try:
            with self.get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute(query, params)
                conn.commit()
                last_id = cursor.lastrowid
                logger.info(f"Insert executed: row ID {last_id}")
                return last_id
        except sqlite3.Error as e:
            logger.error(f"Insert failed: {e}\nQuery: {query}")
            raise DatabaseError(
                f"Insert failed: {str(e)}",
                query=query,
                details={"params": params},
            )

    def execute_transaction(self, queries: List[tuple]) -> bool:
        """
        Execute multiple queries in a transaction.

        Args:
            queries: List of (query, params) tuples

        Returns:
            True if successful, False otherwise

        Example:
            >>> queries = [
            ...     ("INSERT INTO farmers (code, name) VALUES (?, ?)", ("01", "Farmer 1")),
            ...     ("INSERT INTO farmers (code, name) VALUES (?, ?)", ("02", "Farmer 2")),
            ... ]
            >>> db.execute_transaction(queries)
        """
        try:
            with self.get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute("BEGIN TRANSACTION")
                for query, params in queries:
                    cursor.execute(query, params)
                conn.commit()
                logger.info(f"Transaction executed: {len(queries)} queries")
                return True
        except sqlite3.Error as e:
            logger.error(f"Transaction failed: {e}")
            raise DatabaseError(f"Transaction failed: {str(e)}")

    def close_all(self) -> None:
        """
        Close all connections in pool.
        """
        with self.pool_lock:
            for conn in self.pool:
                try:
                    conn.close()
                except sqlite3.Error as e:
                    logger.warning(f"Error closing connection: {e}")
            self.pool.clear()
        logger.info("All database connections closed")

    def __del__(self):
        """Cleanup connections when object is destroyed."""
        self.close_all()


# Global database connection instance
_db_instance: Optional[DatabaseConnection] = None
_db_lock = threading.Lock()


def get_db(db_path: str = None) -> DatabaseConnection:
    """
    Get global database connection instance (singleton).

    Args:
        db_path: Path to database file (only used for first initialization)

    Returns:
        DatabaseConnection instance

    Example:
        >>> db = get_db()
        >>> farmers = db.execute_query("SELECT * FROM farmers")
    """
    global _db_instance

    if _db_instance is None:
        with _db_lock:
            if _db_instance is None:
                _db_instance = DatabaseConnection(db_path)

    return _db_instance
