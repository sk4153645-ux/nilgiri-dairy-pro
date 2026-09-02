"""
Ledger Service

Handles khata (ledger) management and balance calculations.
"""

from typing import Dict, List, Tuple, Any
from datetime import datetime
from src.database.connection import get_db
from src.logger import setup_logger

logger = setup_logger(__name__)


class LedgerService:
    """
    Ledger (Khata) management service.

    Calculates:
        - Running balance for farmers
        - Running balance for customers
        - Outstanding amounts
        - Payment history
    """

    @staticmethod
    def get_farmer_ledger(farmer_code: str) -> Tuple[bool, str, List[Dict]]:
        """
        Get complete ledger for farmer.

        Returns running balance showing:
        - Date, Type (Milk Purchase/Payment), Amount, Balance

        Args:
            farmer_code: Farmer code

        Returns:
            Tuple of (success, message, ledger_entries)
        """
        try:
            db = get_db()

            # Get all milk purchases
            purchases = db.execute_query(
                """
                SELECT
                    date,
                    'Milk Purchase' as type,
                    total_amount as amount,
                    litres,
                    milk_type
                FROM milk_purchases
                WHERE farmer_code = ?
                ORDER BY date ASC, id ASC
                """,
                (farmer_code,),
            )

            # Get all payments
            payments = db.execute_query(
                """
                SELECT
                    date,
                    'Payment' as type,
                    -amount as amount,
                    payment_mode,
                    NULL as litres,
                    NULL as milk_type
                FROM farmer_payments
                WHERE farmer_code = ?
                ORDER BY date ASC, id ASC
                """,
                (farmer_code,),
            )

            # Merge and sort
            entries = [dict(p) for p in purchases] + [dict(p) for p in payments]
            entries.sort(key=lambda x: (x["date"], x["type"]))

            # Calculate running balance
            running_balance = 0.0
            for entry in entries:
                running_balance += entry["amount"]
                entry["balance"] = running_balance

            logger.info(f"Farmer ledger retrieved: {farmer_code}")
            return True, f"Found {len(entries)} entries", entries
        except Exception as e:
            logger.error(f"Failed to get farmer ledger: {e}")
            return False, "Failed to get farmer ledger", []

    @staticmethod
    def get_farmer_outstanding(farmer_code: str) -> Tuple[bool, str, float]:
        """
        Get outstanding amount owed to farmer.

        Args:
            farmer_code: Farmer code

        Returns:
            Tuple of (success, message, outstanding_amount)
        """
        try:
            success, msg, ledger = LedgerService.get_farmer_ledger(farmer_code)
            if not success:
                return False, msg, 0.0

            outstanding = ledger[-1]["balance"] if ledger else 0.0
            return True, "Outstanding calculated", outstanding
        except Exception as e:
            logger.error(f"Failed to calculate outstanding: {e}")
            return False, "Failed to calculate outstanding", 0.0

    @staticmethod
    def get_customer_ledger(customer_code: str) -> Tuple[bool, str, List[Dict]]:
        """
        Get complete ledger for customer.

        Returns running balance showing:
        - Date, Type (Sale/Payment), Amount, Balance

        Args:
            customer_code: Customer code

        Returns:
            Tuple of (success, message, ledger_entries)
        """
        try:
            db = get_db()

            # Get all sales
            sales = db.execute_query(
                """
                SELECT
                    date,
                    'Sale' as type,
                    total_amount as amount,
                    litres,
                    milk_type
                FROM retail_sales
                WHERE customer_code = ?
                ORDER BY date ASC, id ASC
                """,
                (customer_code,),
            )

            # Get all payments
            payments = db.execute_query(
                """
                SELECT
                    date,
                    'Payment' as type,
                    -amount as amount,
                    payment_mode,
                    NULL as litres,
                    NULL as milk_type
                FROM customer_payments
                WHERE customer_code = ?
                ORDER BY date ASC, id ASC
                """,
                (customer_code,),
            )

            # Merge and sort
            entries = [dict(s) for s in sales] + [dict(p) for p in payments]
            entries.sort(key=lambda x: (x["date"], x["type"]))

            # Calculate running balance
            running_balance = 0.0
            for entry in entries:
                running_balance += entry["amount"]
                entry["balance"] = running_balance

            logger.info(f"Customer ledger retrieved: {customer_code}")
            return True, f"Found {len(entries)} entries", entries
        except Exception as e:
            logger.error(f"Failed to get customer ledger: {e}")
            return False, "Failed to get customer ledger", []

    @staticmethod
    def get_customer_outstanding(customer_code: str) -> Tuple[bool, str, float]:
        """
        Get amount owed by customer.

        Args:
            customer_code: Customer code

        Returns:
            Tuple of (success, message, outstanding_amount)
        """
        try:
            success, msg, ledger = LedgerService.get_customer_ledger(customer_code)
            if not success:
                return False, msg, 0.0

            outstanding = ledger[-1]["balance"] if ledger else 0.0
            return True, "Outstanding calculated", outstanding
        except Exception as e:
            logger.error(f"Failed to calculate outstanding: {e}")
            return False, "Failed to calculate outstanding", 0.0
