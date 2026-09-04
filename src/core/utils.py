"""General helper and calculation utilities."""

from datetime import date, datetime
import bcrypt


def calculate_snf(clr: float, fat: float) -> float:
    """Calculates SNF from Corrected Lactometer Reading (CLR) and FAT.
    Standard Indian Dairy Formula: SNF = (CLR / 4) + (0.2 * FAT) + 0.36
    """
    snf = (clr / 4.0) + (0.2 * fat) + 0.36
    return round(snf, 2)


def calculate_milk_rate(
    fat: float,
    snf: float,
    base_fat: float = 6.5,
    base_snf: float = 9.0,
    base_rate: float = 40.0,
) -> float:
    """Calculates milk rate per liter based on two-axis pricing (FAT & SNF)."""
    fat_ratio = fat / base_fat
    snf_ratio = snf / base_snf
    # Equal weightage to FAT & SNF components
    rate = base_rate * (0.6 * fat_ratio + 0.4 * snf_ratio)
    return round(max(rate, 10.0), 2)


def format_currency(amount: float | int) -> str:
    """Formats number as Indian Currency format (₹)."""
    return f"₹{amount:,.2f}"


def format_date(dt: datetime | date | str, fmt: str = "%d-%m-%Y") -> str:
    """Formats datetime to user-facing format."""
    if isinstance(dt, (datetime, date)):
        return dt.strftime(fmt)
    return str(dt)


def hash_password(password: str) -> str:
    """Hashes plain password using bcrypt."""
    salt = bcrypt.gensalt(rounds=12)
    return bcrypt.hashpw(password.encode("utf-8"), salt).decode("utf-8")


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verifies plain password against hashed password."""
    return bcrypt.checkpw(
        plain_password.encode("utf-8"), hashed_password.encode("utf-8")
    )
