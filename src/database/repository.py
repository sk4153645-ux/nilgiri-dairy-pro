"""
Data Access Layer (Repository Pattern)

Provides abstraction over database queries.
Each repository handles queries for a specific entity.
"""

from typing import List, Optional, Dict, Any
from datetime import datetime, date
from src.database.connection import get_db
from src.core.exceptions import DatabaseError, NotFoundError, DuplicateError
from src.logger import setup_logger

logger = setup_logger(__name__)


class FarmerRepository:
    """Repository for farmer data operations."""

    @staticmethod
    def get_by_code(code: str) -> Optional[Dict[str, Any]]:
        """
        Get farmer by code.

        Args:
            code: Farmer code

        Returns:
            Farmer data or None if not found
        """
        db = get_db()
        result = db.execute_query(
            "SELECT * FROM farmers WHERE code = ? AND is_active = 1",
            (code,),
            fetch_one=True,
        )
        return dict(result) if result else None

    @staticmethod
    def get_all() -> List[Dict[str, Any]]:
        """Get all active farmers."""
        db = get_db()
        results = db.execute_query(
            "SELECT * FROM farmers WHERE is_active = 1 ORDER BY CAST(code AS INTEGER) ASC"
        )
        return [dict(row) for row in results]

    @staticmethod
    def create(code: str, name: str, phone: str = "", address: str = "") -> int:
        """
        Create new farmer.

        Args:
            code: Unique farmer code
            name: Farmer name
            phone: Phone number
            address: Address

        Returns:
            Farmer ID

        Raises:
            DuplicateError: If farmer code already exists
        """
        try:
            db = get_db()
            return db.execute_insert(
                "INSERT INTO farmers (code, name, phone, address) VALUES (?, ?, ?, ?)",
                (code, name, phone, address),
            )
        except DatabaseError as e:
            if "UNIQUE constraint failed" in str(e):
                raise DuplicateError("Farmer", "code", code)
            raise

    @staticmethod
    def update_rate(farmer_code: str, rate_type: str, fixed_rate: float = 0.0) -> bool:
        """
        Update farmer's rate type and fixed rate.

        Args:
            farmer_code: Farmer code
            rate_type: 'fixed' or 'variable'
            fixed_rate: Fixed rate if rate_type is 'fixed'

        Returns:
            True if successful
        """
        db = get_db()
        db.execute_update(
            "UPDATE farmers SET rate_type = ?, fixed_rate = ? WHERE code = ?",
            (rate_type, fixed_rate, farmer_code),
        )
        return True


class CustomerRepository:
    """Repository for customer data operations."""

    @staticmethod
    def get_by_code(code: str) -> Optional[Dict[str, Any]]:
        """Get customer by code."""
        db = get_db()
        result = db.execute_query(
            "SELECT * FROM customers WHERE code = ? AND is_active = 1",
            (code,),
            fetch_one=True,
        )
        return dict(result) if result else None

    @staticmethod
    def get_all() -> List[Dict[str, Any]]:
        """Get all active customers."""
        db = get_db()
        results = db.execute_query(
            "SELECT * FROM customers WHERE is_active = 1 ORDER BY CAST(code AS INTEGER) ASC"
        )
        return [dict(row) for row in results]

    @staticmethod
    def create(code: str, name: str, phone: str = "", address: str = "") -> int:
        """
        Create new customer.

        Args:
            code: Unique customer code
            name: Customer name
            phone: Phone number
            address: Address

        Returns:
            Customer ID

        Raises:
            DuplicateError: If customer code already exists
        """
        try:
            db = get_db()
            return db.execute_insert(
                "INSERT INTO customers (code, name, phone, address) VALUES (?, ?, ?, ?)",
                (code, name, phone, address),
            )
        except DatabaseError as e:
            if "UNIQUE constraint failed" in str(e):
                raise DuplicateError("Customer", "code", code)
            raise


class MilkPurchaseRepository:
    """Repository for milk purchase operations."""

    @staticmethod
    def create(
        date: str,
        shift: str,
        farmer_code: str,
        milk_type: str,
        litres: float,
        fat: float,
        snf: float,
        rate: float,
        total_amount: float,
        notes: str = "",
    ) -> int:
        """
        Record milk purchase from farmer.

        Returns:
            Purchase ID
        """
        db = get_db()
        return db.execute_insert(
            """
            INSERT INTO milk_purchases
            (date, shift, farmer_code, milk_type, litres, fat, snf, rate, total_amount, notes)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (date, shift, farmer_code, milk_type, litres, fat, snf, rate, total_amount, notes),
        )

    @staticmethod
    def get_by_date_shift(date: str, shift: str) -> List[Dict[str, Any]]:
        """Get all milk purchases for a date and shift."""
        db = get_db()
        results = db.execute_query(
            "SELECT * FROM milk_purchases WHERE date = ? AND shift = ? ORDER BY id DESC",
            (date, shift),
        )
        return [dict(row) for row in results]

    @staticmethod
    def get_shift_summary(date: str, shift: str) -> Dict[str, Any]:
        """Get summary of milk collection for a shift."""
        db = get_db()
        result = db.execute_query(
            """
            SELECT
                milk_type,
                SUM(litres) as total_litres,
                AVG(fat) as avg_fat,
                SUM(total_amount) as total_amount
            FROM milk_purchases
            WHERE date = ? AND shift = ?
            GROUP BY milk_type
            """,
            (date, shift),
        )
        return [dict(row) for row in result]

    @staticmethod
    def delete(purchase_id: int) -> bool:
        """Delete a milk purchase entry."""
        db = get_db()
        db.execute_update(
            "DELETE FROM milk_purchases WHERE id = ?",
            (purchase_id,),
        )
        return True

    @staticmethod
    def update(purchase_id: int, **kwargs) -> bool:
        """Update milk purchase entry."""
        db = get_db()
        allowed_fields = ["litres", "fat", "snf", "rate", "total_amount", "notes"]
        set_clause = ", ".join([f"{k} = ?" for k in kwargs.keys() if k in allowed_fields])
        values = [kwargs[k] for k in kwargs.keys() if k in allowed_fields]
        values.append(purchase_id)

        db.execute_update(
            f"UPDATE milk_purchases SET {set_clause} WHERE id = ?",
            tuple(values),
        )
        return True
