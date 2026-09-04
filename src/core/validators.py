"""Validation functions for user input and domain constraints."""

from datetime import datetime
import re
from typing import Any
from src.core.exceptions import ValidationError


def sanitize_string(value: str, max_length: int = 255) -> str:
    """Strips whitespace, checks length and blocks common SQL injection patterns."""
    if not value:
        return ""
    val = str(value).strip()
    if len(val) > max_length:
        raise ValidationError("string", f"Length exceeds maximum limit of {max_length}.")

    sql_patterns = [r"(--)", r"(\bDROP\b)", r"(\bSELECT\b)", r"(\bUNION\b)", r"(';)", r"(\bINSERT\b)"]
    for pattern in sql_patterns:
        if re.search(pattern, val, re.IGNORECASE):
            raise ValidationError("string", "Potentially unsafe input detected.")
    return val


class ValidatedTuple(tuple):
    """Allows (is_valid, cleaned) unpacking while also acting as truthy value."""
    def __new__(cls, is_valid: bool, val: Any):
        return super().__new__(cls, (is_valid, val))


def validate_code(code: str, entity_type: str = "general") -> ValidatedTuple:
    if not code:
        raise ValidationError("code", "Code is required.")
    cleaned = str(code).strip().upper()
    if not re.fullmatch(r"[A-Z0-9_-]{2,20}", cleaned):
        raise ValidationError("code", "Code must be 2-20 alphanumeric characters.")
    return ValidatedTuple(True, cleaned)


def validate_phone(phone: str) -> ValidatedTuple:
    if not phone:
        raise ValidationError("phone", "Phone number is required.")
    cleaned = re.sub(r"\s+", "", str(phone).strip())
    if cleaned.startswith("+91"):
        cleaned = cleaned[3:]
    elif cleaned.startswith("0"):
        cleaned = cleaned[1:]

    if not re.fullmatch(r"[6-9]\d{9}", cleaned):
        raise ValidationError("phone", "Invalid mobile number. Must be 10 digits starting with 6-9.")
    return ValidatedTuple(True, cleaned)


validate_phone_number = validate_phone


def validate_email(email: str) -> ValidatedTuple:
    if not email:
        raise ValidationError("email", "Email address is required.")
    cleaned = str(email).strip().lower()
    email_regex = r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$"
    if not re.fullmatch(email_regex, cleaned):
        raise ValidationError("email", "Invalid email address format.")
    return ValidatedTuple(True, cleaned)


def validate_positive_number(
    val: Any,
    field_name: str = "value",
    min_val: float = 0.0,
    max_val: float = 100000.0,
) -> float:
    try:
        num = float(val)
    except (ValueError, TypeError):
        raise ValidationError(field_name, f"{field_name} must be numeric.")

    if num <= min_val or num > max_val:
        raise ValidationError(field_name, f"{field_name} must be between {min_val} and {max_val}.")
    return round(num, 2)


def validate_fat(fat: Any) -> float:
    return validate_positive_number(fat, "fat", min_val=1.99, max_val=15.0)


def validate_snf(snf: Any) -> float:
    return validate_positive_number(snf, "snf", min_val=5.99, max_val=12.0)


def validate_quantity(qty: Any) -> float:
    return validate_positive_number(qty, "quantity", min_val=0.0, max_val=10000.0)


def validate_rate(rate: Any) -> float:
    return validate_positive_number(rate, "rate", min_val=0.0, max_val=1000.0)


def validate_date(date_val: Any, date_format: str = "%Y-%m-%d") -> ValidatedTuple:
    if isinstance(date_val, datetime):
        return ValidatedTuple(True, date_val)
    try:
        parsed = datetime.strptime(str(date_val).strip(), date_format)
        return ValidatedTuple(True, parsed)
    except (ValueError, AttributeError):
        raise ValidationError("date", f"Date must be in format {date_format}.")


def validate_milk_entry(*args, **kwargs) -> Any:
    if len(args) == 4:
        litres, fat, snf, rate = args
        return {
            "litres": validate_quantity(litres),
            "fat": validate_fat(fat),
            "snf": validate_snf(snf),
            "rate": validate_rate(rate),
        }
    if args and isinstance(args[0], dict):
        data = args[0]
        if "litres" in data:
            data["litres"] = validate_quantity(data["litres"])
        if "fat" in data:
            data["fat"] = validate_fat(data["fat"])
        if "snf" in data:
            data["snf"] = validate_snf(data["snf"])
        if "rate" in data:
            data["rate"] = validate_rate(data["rate"])
        return data
    return True
