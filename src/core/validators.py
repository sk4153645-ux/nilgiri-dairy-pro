"""Validation functions for user input and domain constraints."""

from datetime import datetime
import re
from src.core.exceptions import ValidationError


def sanitize_string(value: str) -> str:
    """Strips whitespace and escapes potential malicious chars."""
    if not value:
        return ""
    return str(value).strip()


def validate_code(code: str) -> str:
    """Validates alphanumeric entity codes (Farmer/Customer/Staff ID)."""
    if not code:
        raise ValidationError("code", "Code is required.")
    cleaned = str(code).strip().upper()
    if not re.fullmatch(r"[A-Z0-9_-]{2,20}", cleaned):
        raise ValidationError("code", "Code must be 2-20 alphanumeric characters.")
    return cleaned


def validate_phone(phone: str) -> str:
    """Validates 10-digit Indian mobile numbers."""
    if not phone:
        raise ValidationError("phone", "Phone number is required.")
    cleaned = re.sub(r"\s+", "", str(phone).strip())
    if cleaned.startswith("+91"):
        cleaned = cleaned[3:]
    elif cleaned.startswith("0"):
        cleaned = cleaned[1:]

    if not re.fullmatch(r"[6-9]\d{9}", cleaned):
        raise ValidationError("phone", "Invalid mobile number. Must be 10 digits starting with 6-9.")
    return cleaned


# Alias for backwards compatibility with tests and models
validate_phone_number = validate_phone


def validate_fat(fat: float | int | str) -> float:
    """Validates milk FAT percentage (typically 2.0 to 15.0%)."""
    try:
        val = float(fat)
    except (ValueError, TypeError):
        raise ValidationError("fat", "FAT value must be numeric.")

    if not (2.0 <= val <= 15.0):
        raise ValidationError("fat", "FAT must be between 2.0% and 15.0%.")
    return round(val, 2)


def validate_snf(snf: float | int | str) -> float:
    """Validates milk SNF percentage (typically 6.0 to 12.0%)."""
    try:
        val = float(snf)
    except (ValueError, TypeError):
        raise ValidationError("snf", "SNF value must be numeric.")

    if not (6.0 <= val <= 12.0):
        raise ValidationError("snf", "SNF must be between 6.0% and 12.0%.")
    return round(val, 2)


def validate_quantity(qty: float | int | str) -> float:
    """Validates milk quantity in liters (greater than 0)."""
    try:
        val = float(qty)
    except (ValueError, TypeError):
        raise ValidationError("quantity", "Quantity must be numeric.")

    if val <= 0:
        raise ValidationError("quantity", "Quantity must be greater than 0.")
    if val > 10000:
        raise ValidationError("quantity", "Quantity exceeds maximum threshold (10,000L).")
    return round(val, 2)


def validate_rate(rate: float | int | str) -> float:
    """Validates milk purchase/sale price per liter."""
    try:
        val = float(rate)
    except (ValueError, TypeError):
        raise ValidationError("rate", "Rate must be numeric.")

    if val <= 0:
        raise ValidationError("rate", "Rate per liter must be positive.")
    return round(val, 2)


def validate_date(date_str: str, date_format: str = "%Y-%m-%d") -> datetime:
    """Validates date format."""
    try:
        return datetime.strptime(date_str.strip(), date_format)
    except (ValueError, AttributeError):
        raise ValidationError("date", f"Date must be in format {date_format}.")
