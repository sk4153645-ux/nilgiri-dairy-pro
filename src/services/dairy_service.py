"""
Dairy Service

Core business logic for dairy operations.
"""

from typing import Dict, List, Any, Tuple
from datetime import datetime, date
from src.database.connection import get_db
from src.database.repository import (
    FarmerRepository,
    CustomerRepository,
    MilkPurchaseRepository,
)
from src.models.farmer import Farmer
from src.models.customer import Customer
from src.models.milk_entry import MilkEntry
from src.core.exceptions import (
    ValidationError,
    NotFoundError,
    DuplicateError,
    BusinessLogicError,
)
from src.logger import setup_logger

logger = setup_logger(__name__)


class DairyService:
    """
    Core dairy business logic service.

    Handles:
        - Farmer management
        - Milk collection
        - Sales tracking
        - Payment settlements
    """

    # === FARMER OPERATIONS ===

    @staticmethod
    def create_farmer(
        code: str, name: str, phone: str = "", address: str = ""
    ) -> Tuple[bool, str, int]:
        """
        Create new farmer.

        Args:
            code: Farmer code
            name: Farmer name
            phone: Phone number
            address: Address

        Returns:
            Tuple of (success, message, farmer_id)
        """
        try:
            farmer = Farmer(code=code, name=name, phone=phone, address=address)
            is_valid, error = farmer.validate()
            if not is_valid:
                return False, error, 0

            farmer_id = FarmerRepository.create(
                code=farmer.code,
                name=farmer.name,
                phone=farmer.phone,
                address=farmer.address,
            )
            logger.info(f"Farmer created: {code} - {name}")
            return True, "Farmer created successfully", farmer_id
        except DuplicateError as e:
            logger.warning(f"Duplicate farmer: {e}")
            return False, str(e), 0
        except Exception as e:
            logger.error(f"Failed to create farmer: {e}")
            return False, "Failed to create farmer", 0

    @staticmethod
    def get_farmer(code: str) -> Tuple[bool, str, Optional[Dict]]:
        """
        Get farmer details.

        Args:
            code: Farmer code

        Returns:
            Tuple of (success, message, farmer_data)
        """
        try:
            farmer = FarmerRepository.get_by_code(code)
            if not farmer:
                return False, f"Farmer not found: {code}", None
            return True, "Farmer found", farmer
        except Exception as e:
            logger.error(f"Failed to get farmer: {e}")
            return False, "Failed to get farmer", None

    @staticmethod
    def list_farmers() -> Tuple[bool, str, List[Dict]]:
        """
        List all farmers.

        Returns:
            Tuple of (success, message, farmers_list)
        """
        try:
            farmers = FarmerRepository.get_all()
            return True, f"Found {len(farmers)} farmers", farmers
        except Exception as e:
            logger.error(f"Failed to list farmers: {e}")
            return False, "Failed to list farmers", []

    # === MILK COLLECTION ===

    @staticmethod
    def record_milk_purchase(
        date: str,
        shift: str,
        farmer_code: str,
        milk_type: str,
        litres: float,
        fat: float = 0.0,
        snf: float = 0.0,
        rate: float = 0.0,
        notes: str = "",
    ) -> Tuple[bool, str, int]:
        """
        Record milk purchase from farmer.

        Args:
            date: Purchase date (YYYY-MM-DD)
            shift: Morning or Evening
            farmer_code: Farmer code
            milk_type: Cow or Buffalo
            litres: Quantity
            fat: Fat percentage
            snf: SNF value
            rate: Rate per litre
            notes: Notes

        Returns:
            Tuple of (success, message, purchase_id)
        """
        try:
            # Validate farmer exists
            farmer = FarmerRepository.get_by_code(farmer_code)
            if not farmer:
                return False, f"Farmer not found: {farmer_code}", 0

            # Validate milk entry
            milk_entry = MilkEntry(
                date=date,
                shift=shift,
                milk_type=milk_type,
                litres=litres,
                fat=fat,
                snf=snf,
                rate=rate,
            )
            is_valid, error = milk_entry.validate()
            if not is_valid:
                return False, error, 0

            # Use farmer's fixed rate if available
            if farmer["rate_type"] == "fixed" and farmer["fixed_rate"] > 0:
                rate = farmer["fixed_rate"]

            total_amount = milk_entry.calculate_total()

            # Record purchase
            purchase_id = MilkPurchaseRepository.create(
                date=date,
                shift=shift,
                farmer_code=farmer_code,
                milk_type=milk_type,
                litres=litres,
                fat=fat,
                snf=snf,
                rate=rate,
                total_amount=total_amount,
                notes=notes,
            )

            logger.info(
                f"Milk purchase recorded: {farmer_code} - {litres}L @ {rate}/L = {total_amount}"
            )
            return True, f"Milk purchase recorded: ₹{total_amount:.2f}", purchase_id
        except Exception as e:
            logger.error(f"Failed to record milk purchase: {e}")
            return False, "Failed to record milk purchase", 0

    @staticmethod
    def get_daily_collection(date: str, shift: str) -> Tuple[bool, str, Dict]:
        """
        Get daily milk collection summary.

        Args:
            date: Date (YYYY-MM-DD)
            shift: Morning or Evening

        Returns:
            Tuple of (success, message, summary_data)
        """
        try:
            db = get_db()
            summary = db.execute_query(
                """
                SELECT
                    milk_type,
                    COUNT(*) as count,
                    SUM(litres) as total_litres,
                    AVG(fat) as avg_fat,
                    SUM(total_amount) as total_amount
                FROM milk_purchases
                WHERE date = ? AND shift = ?
                GROUP BY milk_type
                """,
                (date, shift),
            )

            if not summary:
                return True, "No collection data", {}

            data = {row["milk_type"]: dict(row) for row in summary}
            return True, "Summary retrieved", data
        except Exception as e:
            logger.error(f"Failed to get daily collection: {e}")
            return False, "Failed to get daily collection", {}

    # === CUSTOMER OPERATIONS ===

    @staticmethod
    def create_customer(
        code: str, name: str, phone: str = "", address: str = ""
    ) -> Tuple[bool, str, int]:
        """
        Create new customer.

        Args:
            code: Customer code
            name: Customer name
            phone: Phone number
            address: Address

        Returns:
            Tuple of (success, message, customer_id)
        """
        try:
            customer = Customer(code=code, name=name, phone=phone, address=address)
            is_valid, error = customer.validate()
            if not is_valid:
                return False, error, 0

            customer_id = CustomerRepository.create(
                code=customer.code,
                name=customer.name,
                phone=customer.phone,
                address=customer.address,
            )
            logger.info(f"Customer created: {code} - {name}")
            return True, "Customer created successfully", customer_id
        except DuplicateError as e:
            logger.warning(f"Duplicate customer: {e}")
            return False, str(e), 0
        except Exception as e:
            logger.error(f"Failed to create customer: {e}")
            return False, "Failed to create customer", 0

    @staticmethod
    def list_customers() -> Tuple[bool, str, List[Dict]]:
        """
        List all customers.

        Returns:
            Tuple of (success, message, customers_list)
        """
        try:
            customers = CustomerRepository.get_all()
            return True, f"Found {len(customers)} customers", customers
        except Exception as e:
            logger.error(f"Failed to list customers: {e}")
            return False, "Failed to list customers", []

    # === PAYMENT OPERATIONS ===

    @staticmethod
    def settle_farmer_payment(
        date: str, farmer_code: str, amount: float, payment_mode: str, reference: str = ""
    ) -> Tuple[bool, str]:
        """
        Record farmer payment/settlement.

        Args:
            date: Payment date
            farmer_code: Farmer code
            amount: Payment amount
            payment_mode: Cash, Online, etc.
            reference: Payment reference

        Returns:
            Tuple of (success, message)
        """
        try:
            # Verify farmer exists
            farmer = FarmerRepository.get_by_code(farmer_code)
            if not farmer:
                return False, f"Farmer not found: {farmer_code}"

            # Validate amount
            if amount <= 0:
                return False, "Payment amount must be positive"

            # Record payment
            db = get_db()
            db.execute_insert(
                """
                INSERT INTO farmer_payments (date, farmer_code, amount, payment_mode, reference)
                VALUES (?, ?, ?, ?, ?)
                """,
                (date, farmer_code, amount, payment_mode, reference),
            )

            logger.info(
                f"Farmer payment recorded: {farmer_code} - {payment_mode} - ₹{amount:.2f}"
            )
            return True, f"Payment recorded: ₹{amount:.2f} via {payment_mode}"
        except Exception as e:
            logger.error(f"Failed to record payment: {e}")
            return False, "Failed to record payment"
