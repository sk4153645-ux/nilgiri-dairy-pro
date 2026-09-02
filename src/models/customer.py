"""
Customer Model

Represents a customer (milk buyer) in the system.
"""

from typing import Tuple
from src.models.base import BaseModel
from src.core.validators import validate_code, validate_phone_number, sanitize_string
from src.core.exceptions import ValidationError


class Customer(BaseModel):
    """
    Customer model with validation.

    Attributes:
        code: Unique customer code
        name: Customer name
        phone: Phone number
        address: Address
        credit_limit: Maximum credit allowed
        is_active: Whether customer is active
    """

    def __init__(
        self,
        code: str,
        name: str,
        phone: str = "",
        address: str = "",
        credit_limit: float = 0.0,
        is_active: bool = True,
    ):
        """
        Initialize Customer model.

        Args:
            code: Unique customer code
            name: Customer name
            phone: Phone number
            address: Address
            credit_limit: Credit limit
            is_active: Active status
        """
        self.code = code
        self.name = name
        self.phone = phone
        self.address = address
        self.credit_limit = credit_limit
        self.is_active = is_active

    def validate(self) -> Tuple[bool, str]:
        """
        Validate customer data.

        Returns:
            Tuple of (is_valid, error_message)
        """
        try:
            # Validate code
            _, self.code = validate_code(self.code, "customer")

            # Validate name
            self.name = sanitize_string(self.name, max_length=100)
            if not self.name:
                raise ValidationError("Customer name is required", field="name")

            # Validate phone if provided
            if self.phone:
                _, self.phone = validate_phone_number(self.phone)

            # Validate address if provided
            if self.address:
                self.address = sanitize_string(self.address, max_length=255)

            # Validate credit limit
            if self.credit_limit < 0:
                raise ValidationError(
                    "Credit limit cannot be negative", field="credit_limit"
                )

            return True, ""
        except ValidationError as e:
            return False, str(e)
