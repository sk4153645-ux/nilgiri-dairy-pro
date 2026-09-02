"""
Farmer Model

Represents a farmer in the system.
"""

from typing import Optional, Tuple
from src.models.base import BaseModel
from src.core.validators import validate_code, validate_phone_number, sanitize_string
from src.core.exceptions import ValidationError


class Farmer(BaseModel):
    """
    Farmer model with validation.

    Attributes:
        code: Unique farmer code
        name: Farmer name
        phone: Phone number
        address: Address (optional)
        rate_type: 'fixed' or 'variable'
        fixed_rate: Fixed rate per litre (if rate_type is 'fixed')
        is_active: Whether farmer is active
    """

    def __init__(
        self,
        code: str,
        name: str,
        phone: str = "",
        address: str = "",
        rate_type: str = "variable",
        fixed_rate: float = 0.0,
        is_active: bool = True,
    ):
        """
        Initialize Farmer model.

        Args:
            code: Unique farmer code
            name: Farmer name
            phone: Phone number
            address: Address
            rate_type: 'fixed' or 'variable'
            fixed_rate: Fixed rate per litre
            is_active: Active status
        """
        self.code = code
        self.name = name
        self.phone = phone
        self.address = address
        self.rate_type = rate_type
        self.fixed_rate = fixed_rate
        self.is_active = is_active

    def validate(self) -> Tuple[bool, str]:
        """
        Validate farmer data.

        Returns:
            Tuple of (is_valid, error_message)
        """
        try:
            # Validate code
            _, self.code = validate_code(self.code, "farmer")

            # Validate name
            self.name = sanitize_string(self.name, max_length=100)
            if not self.name:
                raise ValidationError("Farmer name is required", field="name")

            # Validate phone if provided
            if self.phone:
                _, self.phone = validate_phone_number(self.phone)

            # Validate address if provided
            if self.address:
                self.address = sanitize_string(self.address, max_length=255)

            # Validate rate type
            if self.rate_type not in ["fixed", "variable"]:
                raise ValidationError(
                    "Rate type must be 'fixed' or 'variable'",
                    field="rate_type",
                )

            # Validate fixed rate if rate_type is 'fixed'
            if self.rate_type == "fixed":
                if self.fixed_rate <= 0:
                    raise ValidationError(
                        "Fixed rate must be greater than 0", field="fixed_rate"
                    )
                if self.fixed_rate > 1000:
                    raise ValidationError(
                        "Fixed rate seems too high (> 1000)", field="fixed_rate"
                    )

            return True, ""
        except ValidationError as e:
            return False, str(e)

    def get_rate(self, variable_rate: float = 0.0) -> float:
        """
        Get applicable rate for this farmer.

        Args:
            variable_rate: Current variable rate

        Returns:
            Rate to apply for milk purchase
        """
        if self.rate_type == "fixed":
            return self.fixed_rate
        return variable_rate
