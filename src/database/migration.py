"""
Database Migrations

Handles database schema creation and migrations.
Provides version control for database structure.
"""

import sqlite3
from pathlib import Path
from typing import List
from src.logger import setup_logger
from src.core.exceptions import DatabaseError

logger = setup_logger(__name__)


class DatabaseMigration:
    """
    Database migration and schema management.

    Handles:
        - Initial schema creation
        - Schema migrations
        - Version tracking
        - Data integrity checks
    """

    # SQL queries for schema creation
    SCHEMA = [
        # Users table
        """
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            email TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL,
            dairy_name TEXT DEFAULT 'Nilgiri Dairy',
            dairy_phone TEXT,
            is_active BOOLEAN DEFAULT 1,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        """,
        # Farmers table
        """
        CREATE TABLE IF NOT EXISTS farmers (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            code TEXT UNIQUE NOT NULL,
            name TEXT NOT NULL,
            phone TEXT,
            address TEXT,
            rate_type TEXT DEFAULT 'variable',
            fixed_rate REAL DEFAULT 0.0,
            is_active BOOLEAN DEFAULT 1,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        """,
        # Customers table
        """
        CREATE TABLE IF NOT EXISTS customers (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            code TEXT UNIQUE NOT NULL,
            name TEXT NOT NULL,
            phone TEXT,
            address TEXT,
            credit_limit REAL DEFAULT 0.0,
            is_active BOOLEAN DEFAULT 1,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        """,
        # Milk purchases (from farmers)
        """
        CREATE TABLE IF NOT EXISTS milk_purchases (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            date TEXT NOT NULL,
            shift TEXT NOT NULL,
            farmer_code TEXT NOT NULL,
            milk_type TEXT NOT NULL,
            litres REAL NOT NULL,
            fat REAL DEFAULT 0.0,
            snf REAL DEFAULT 0.0,
            rate REAL NOT NULL,
            total_amount REAL NOT NULL,
            is_settled BOOLEAN DEFAULT 0,
            notes TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (farmer_code) REFERENCES farmers(code)
        )
        """,
        # Retail sales (to customers)
        """
        CREATE TABLE IF NOT EXISTS retail_sales (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            date TEXT NOT NULL,
            shift TEXT NOT NULL,
            customer_code TEXT NOT NULL,
            milk_type TEXT NOT NULL,
            litres REAL NOT NULL,
            rate REAL NOT NULL,
            total_amount REAL NOT NULL,
            is_paid BOOLEAN DEFAULT 0,
            notes TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (customer_code) REFERENCES customers(code)
        )
        """,
        # Farmer payments (settlements)
        """
        CREATE TABLE IF NOT EXISTS farmer_payments (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            date TEXT NOT NULL,
            farmer_code TEXT NOT NULL,
            amount REAL NOT NULL,
            payment_mode TEXT NOT NULL,
            reference TEXT,
            notes TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (farmer_code) REFERENCES farmers(code)
        )
        """,
        # Customer payments
        """
        CREATE TABLE IF NOT EXISTS customer_payments (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            date TEXT NOT NULL,
            customer_code TEXT NOT NULL,
            amount REAL NOT NULL,
            payment_mode TEXT NOT NULL,
            reference TEXT,
            notes TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (customer_code) REFERENCES customers(code)
        )
        """,
        # Audit log (tracks all changes)
        """
        CREATE TABLE IF NOT EXISTS audit_log (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            table_name TEXT NOT NULL,
            record_id INTEGER NOT NULL,
            action TEXT NOT NULL,
            old_value TEXT,
            new_value TEXT,
            user_id INTEGER,
            ip_address TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        """,
        # Application settings
        """
        CREATE TABLE IF NOT EXISTS settings (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            key TEXT UNIQUE NOT NULL,
            value TEXT NOT NULL,
            description TEXT,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        """,
        # Indexes for performance
        "CREATE INDEX IF NOT EXISTS idx_farmers_code ON farmers(code)",
        "CREATE INDEX IF NOT EXISTS idx_customers_code ON customers(code)",
        "CREATE INDEX IF NOT EXISTS idx_milk_purchases_date ON milk_purchases(date)",
        "CREATE INDEX IF NOT EXISTS idx_milk_purchases_farmer ON milk_purchases(farmer_code)",
        "CREATE INDEX IF NOT EXISTS idx_retail_sales_date ON retail_sales(date)",
        "CREATE INDEX IF NOT EXISTS idx_retail_sales_customer ON retail_sales(customer_code)",
        "CREATE INDEX IF NOT EXISTS idx_payments_date ON farmer_payments(date)",
        "CREATE INDEX IF NOT EXISTS idx_audit_log_table ON audit_log(table_name)",
    ]

    @staticmethod
    def initialize(db_path: str) -> bool:
        """
        Initialize database with schema.

        Args:
            db_path: Path to SQLite database file

        Returns:
            True if successful

        Raises:
            DatabaseError: If initialization fails
        """
        try:
            # Create parent directory if it doesn't exist
            Path(db_path).parent.mkdir(parents=True, exist_ok=True)

            conn = sqlite3.connect(db_path)
            cursor = conn.cursor()

            # Execute all schema creation queries
            for query in DatabaseMigration.SCHEMA:
                cursor.execute(query)

            conn.commit()
            conn.close()
            logger.info(f"Database initialized successfully at {db_path}")
            return True
        except sqlite3.Error as e:
            logger.error(f"Database initialization failed: {e}")
            raise DatabaseError(f"Failed to initialize database: {str(e)}")

    @staticmethod
    def reset(db_path: str) -> bool:
        """
        Drop all tables and reinitialize database.

        Args:
            db_path: Path to SQLite database file

        Returns:
            True if successful

        Warning:
            This will delete all data!
        """
        try:
            conn = sqlite3.connect(db_path)
            cursor = conn.cursor()

            # Get all table names
            cursor.execute(
                "SELECT name FROM sqlite_master WHERE type='table' AND name NOT LIKE 'sqlite_%'"
            )
            tables = cursor.fetchall()

            # Drop all tables
            for table in tables:
                cursor.execute(f"DROP TABLE IF EXISTS {table[0]}")

            conn.commit()
            conn.close()

            # Reinitialize schema
            DatabaseMigration.initialize(db_path)
            logger.warning(f"Database reset and reinitialized")
            return True
        except sqlite3.Error as e:
            logger.error(f"Database reset failed: {e}")
            raise DatabaseError(f"Failed to reset database: {str(e)}")

    @staticmethod
    def add_sample_data(db_path: str) -> bool:
        """
        Add sample data for testing.

        Args:
            db_path: Path to SQLite database file

        Returns:
            True if successful
        """
        try:
            conn = sqlite3.connect(db_path)
            cursor = conn.cursor()

            # Sample farmers
            sample_farmers = [
                ("01", "Ramesh Kumar", "9876543210", "variable", 0),
                ("02", "Suresh Singh", "9876543211", "variable", 0),
                ("03", "Vikram Patel", "9876543212", "fixed", 45.0),
            ]

            cursor.executemany(
                "INSERT INTO farmers (code, name, phone, rate_type, fixed_rate) VALUES (?, ?, ?, ?, ?)",
                sample_farmers,
            )

            # Sample customers
            sample_customers = [
                ("C01", "Rajesh Sharma", "9876543220"),
                ("C02", "Priya Desai", "9876543221"),
            ]

            cursor.executemany(
                "INSERT INTO customers (code, name, phone) VALUES (?, ?, ?)",
                sample_customers,
            )

            conn.commit()
            conn.close()
            logger.info("Sample data added successfully")
            return True
        except sqlite3.Error as e:
            logger.error(f"Failed to add sample data: {e}")
            return False
