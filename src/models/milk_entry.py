"""
Milk Entry Model

Represents a milk purchase or sale transaction.
"""

from typing import Tuple
from src.models.base import BaseModel
from src.core.validators import validate_positive_number, validate_date
from src.core.exceptions import ValidationError


class MilkEntry(BaseModel):
    """
    Milk entry model for purchases and sales.

    Attributes:
        date: Transaction date
        shift: Morning or Evening
        milk_type: Cow or Buffalo
        litres: Quantity in litres
        fat: Fat percentage
        snf: SNF/CLR value
        rate: Rate per litre
        total_amount: Total amount (calculated)
    """

    def __init__(
        self,
        date: str,
        shift: str,
        milk_type: str,
        litres: float,
        fat: float = 0.0,
        snf: float = 0.0,
        rate: float = 0.0,
    ):
        """
        Initialize MilkEntry model.

        Args:
            date: Transaction date (YYYY-MM-DD)
            shift: Morning or Evening
            milk_type: Cow or Buffalo
            litres: Quantity in litres
            fat: Fat percentage (optional)
            snf: SNF/CLR value (optional)
            rate: Rate per litre (optional)
        """
        self.date = date
        self.shift = shift
        self.milk_type = milk_type
        self.litres = litres
        self.fat = fat
        self.snf = snf
        self.rate = rate

    def validate(self) -> Tuple[bool, str]:
        """
        Validate milk entry data.

        Returns:
            Tuple of (is_valid, error_message)
        """
        try:
            # Validate date
            _, self.date = validate_date(self.date)

            # Validate shift
            if self.shift not in ["Morning", "Evening"]:
                raise ValidationError(
                    "Shift must be 'Morning' or 'Evening'", field="shift"
                )

            # Validate milk type
            if self.milk_type not in ["Cow", "Buffalo"]:
                raise ValidationError(
                    "Milk type must be 'Cow' or 'Buffalo'", field="milk_type"
                )

            # Validate litres (required, 0.1-100)
            self.litres = validate_positive_number(
                self.litres, "litres", min_val=0.1, max_val=100
            )

            # Validate fat (0-8%)
            if self.fat:
                self.fat = validate_positive_number(
                    self.fat, "fat", min_val=0, max_val=8
                )

            # Validate SNF (7-10%)
            if self.snf:
                self.snf = validate_positive_number(
                    self.snf, "snf", min_val=7, max_val=10
                )

            # Validate rate (if provided)
            if self.rate:
                self.rate = validate_positive_number(
                    self.rate, "rate", min_val=0, max_val=1000
                )

            return True, ""
        except ValidationError as e:
            return False, str(e)

    def calculate_total(self) -> float:
        """
        Calculate total amount.

        Returns:
            Total amount (litres * rate)
        """
        return round(self.litres * self.rate, 2)
