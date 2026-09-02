"""
Payment Model

Represents a payment transaction.
"""

from typing import Tuple
from src.models.base import BaseModel
from src.core.validators import validate_positive_number, validate_date
from src.core.exceptions import ValidationError


class Payment(BaseModel):
    """
    Payment model for settlements.

    Attributes:
        date: Payment date
        entity_code: Farmer or customer code
        amount: Payment amount
        payment_mode: Cash, Online, Check, etc.
        reference: Transaction reference (optional)
        notes: Additional notes (optional)
    """

    def __init__(
        self,
        date: str,
        entity_code: str,
        amount: float,
        payment_mode: str,
        reference: str = "",
        notes: str = "",
    ):
        """
        Initialize Payment model.

        Args:
            date: Payment date (YYYY-MM-DD)
            entity_code: Farmer or customer code
            amount: Payment amount
            payment_mode: Payment method
            reference: Transaction reference
            notes: Notes
        """
        self.date = date
        self.entity_code = entity_code
        self.amount = amount
        self.payment_mode = payment_mode
        self.reference = reference
        self.notes = notes

    def validate(self) -> Tuple[bool, str]:
        """
        Validate payment data.

        Returns:
            Tuple of (is_valid, error_message)
        """
        try:
            # Validate date
            _, self.date = validate_date(self.date)

            # Validate entity code
            if not self.entity_code:
                raise ValidationError(
                    "Entity code (farmer/customer) is required", field="entity_code"
                )

            # Validate amount
            self.amount = validate_positive_number(
                self.amount, "amount", min_val=0.01, max_val=1000000
            )

            # Validate payment mode
            valid_modes = ["Cash", "Online", "Check", "UPI", "Bank Transfer"]
            if self.payment_mode not in valid_modes:
                raise ValidationError(
                    f"Payment mode must be one of {valid_modes}",
                    field="payment_mode",
                )

            return True, ""
        except ValidationError as e:
            return False, str(e)
