"""Validation functions for user input and domain constraints."""

from datetime import datetime
import re
from src.core.exceptions import ValidationError


def sanitize_string(value: str) -> str:
    """Strips whitespace and escapes potential malicious chars."""
    if not value:
        return ""
    return str(value).strip()


def validate_email(email: str) -> str:
    """Validates standard email addresses."""
    if not email:
        raise ValidationError("email", "Email address is required.")
    cleaned = str(email).strip().lower()
    email_regex = r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$"
    if not re.fullmatch(email_regex, cleaned):
        raise ValidationError("email", "Invalid email address format.")
    return cleaned
def validate_milk_entry(data: dict) -> dict:
    """Validates complete milk collection entry payload."""
    if not isinstance(data, dict):
        raise ValidationError("entry", "Entry payload must be a dictionary.")

    if "quantity" in data:
        data["quantity"] = validate_quantity(data["quantity"])
    if "fat" in data:
        data["fat"] = validate_fat(data["fat"])
    if "snf" in data:
        data["snf"] = validate_snf(data["snf"])
    if "rate" in data:
        data["rate"] = validate_rate(data["rate"])
    if "date" in data and isinstance(data["date"], str):
        data["date"] = validate_date(data["date"])

    return data

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


validate_phone_number = validate_phone


def validate_positive_number(val: float | int | str, field_name: str = "value") -> float:
    """Validates that a numeric value is strictly greater than zero."""
    try:
        num = float(val)
    except (ValueError, TypeError):
        raise ValidationError(field_name, f"{field_name} must be numeric.")

    if num <= 0:
        raise ValidationError(field_name, f"{field_name} must be greater than zero.")
    return round(num, 2)


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
    return validate_positive_number(qty, "quantity")


def validate_rate(rate: float | int | str) -> float:
    """Validates milk purchase/sale price per liter."""
    return validate_positive_number(rate, "rate")


def validate_date(date_str: str, date_format: str = "%Y-%m-%d") -> datetime:
    """Validates date format."""
    try:
        return datetime.strptime(date_str.strip(), date_format)
    except (ValueError, AttributeError):
        raise ValidationError("date", f"Date must be in format {date_format}.")
