"""Validation functions for user input and domain constraints."""

from datetime import datetime
import re
from typing import Any
from src.core.exceptions import ValidationError


def sanitize_string(value: str, max_length: int = 255) -> str:
    if not value:
        return ""
    val = str(value).strip()
    if len(val) > max_length:
        raise ValidationError("Length exceeds limit", field="string")

    sql_patterns = [r"(--)", r"(\bDROP\b)", r"(\bSELECT\b)", r"(\bUNION\b)", r"(';)", r"(\bINSERT\b)"]
    for pattern in sql_patterns:
        if re.search(pattern, val, re.IGNORECASE):
            raise ValidationError("Potentially unsafe input detected", field="string")
    return val


class ValidatedTuple(tuple):
    def __new__(cls, is_valid: bool, val: Any):
        return super().__new__(cls, (is_valid, val))


def validate_code(code: str, entity_type: str = "general") -> ValidatedTuple:
    if not code:
        raise ValidationError("Code is required", field="code")
    cleaned = str(code).strip().upper()
    if not re.fullmatch(r"[A-Z0-9_-]{2,20}", cleaned):
        raise ValidationError("Code must be 2-20 alphanumeric characters", field="code")
    return ValidatedTuple(True, cleaned)


def validate_phone(phone: str) -> ValidatedTuple:
    if not phone:
        raise ValidationError("Phone number is required", field="phone")
    cleaned = re.sub(r"\s+", "", str(phone).strip())
    if cleaned.startswith("+91"):
        digits = cleaned[3:]
    elif cleaned.startswith("0"):
        digits = cleaned[1:]
    else:
        digits = cleaned

    if not re.fullmatch(r"[6-9]\d{9}", digits):
        raise ValidationError("Invalid mobile number", field="phone")

    return ValidatedTuple(True, f"+91{digits}")


validate_phone_number = validate_phone


def validate_email(email: str) -> ValidatedTuple:
    if not email:
        raise ValidationError("Email is required", field="email")
    cleaned = str(email).strip().lower()
    email_regex = r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$"
    if not re.fullmatch(email_regex, cleaned):
        raise ValidationError("Invalid email address format", field="email")
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
        raise ValidationError(f"{field_name} must be numeric", field=field_name)

    if num < min_val or num > max_val:
        raise ValidationError(f"{field_name} must be between {min_val} and {max_val}", field=field_name)
    return round(num, 2)


def validate_fat(fat: Any) -> float:
    return validate_positive_number(fat, "fat", min_val=0.0, max_val=15.0)


def validate_snf(snf: Any) -> float:
    return validate_positive_number(snf, "snf", min_val=0.0, max_val=12.0)


def validate_quantity(qty: Any) -> float:
    return validate_positive_number(qty, "litres", min_val=0.1, max_val=100.0)


def validate_rate(rate: Any) -> float:
    return validate_positive_number(rate, "rate", min_val=0.1, max_val=1000.0)


def validate_date(date_val: Any, date_format: str = "%Y-%m-%d") -> ValidatedTuple:
    if isinstance(date_val, datetime):
        return ValidatedTuple(True, date_val)
    try:
        parsed = datetime.strptime(str(date_val).strip(), date_format)
        return ValidatedTuple(True, parsed)
    except (ValueError, AttributeError):
        raise ValidationError(f"Date must be in format {date_format}", field="date")


def validate_milk_entry(*args, **kwargs) -> Any:
    data = {}
    if args and isinstance(args[0], dict):
        data = dict(args[0])
    elif kwargs:
        data = dict(kwargs)
    elif len(args) == 4:
        litres, fat, snf, rate = args
        data = {"litres": litres, "fat": fat, "snf": snf, "rate": rate}
    elif len(args) == 1:
        data = {"litres": args[0]}

    if "litres" in data:
        data["litres"] = validate_quantity(data["litres"])
    elif "quantity" in data:
        data["quantity"] = validate_quantity(data["quantity"])

    if "fat" in data and data["fat"] is not None:
        data["fat"] = validate_fat(data["fat"])

    if "snf" in data and data["snf"] is not None:
        data["snf"] = validate_snf(data["snf"])

    if "rate" in data and data["rate"] is not None:
        data["rate"] = validate_rate(data["rate"])

    return data
