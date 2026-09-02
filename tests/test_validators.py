"""
Validator Tests

Tests for input validation functions.
"""

import pytest
from src.core.validators import (
    validate_phone_number,
    validate_email,
    validate_positive_number,
    validate_code,
    validate_date,
    validate_milk_entry,
    sanitize_string,
)
from src.core.exceptions import ValidationError


class TestPhoneValidation:
    """Tests for phone number validation."""

    def test_valid_10_digit_phone(self):
        """Test valid 10-digit phone number."""
        is_valid, cleaned = validate_phone_number("9876543210")
        assert is_valid
        assert cleaned == "+919876543210"

    def test_valid_phone_with_country_code(self):
        """Test valid phone with country code."""
        is_valid, cleaned = validate_phone_number("+919876543210")
        assert is_valid
        assert cleaned == "+919876543210"

    def test_invalid_phone_too_short(self):
        """Test phone number too short."""
        with pytest.raises(ValidationError):
            validate_phone_number("123")

    def test_invalid_phone_empty(self):
        """Test empty phone number."""
        with pytest.raises(ValidationError):
            validate_phone_number("")


class TestEmailValidation:
    """Tests for email validation."""

    def test_valid_email(self):
        """Test valid email."""
        is_valid, cleaned = validate_email("test@example.com")
        assert is_valid
        assert cleaned == "test@example.com"

    def test_invalid_email_no_at(self):
        """Test email without @."""
        with pytest.raises(ValidationError):
            validate_email("testexample.com")

    def test_invalid_email_empty(self):
        """Test empty email."""
        with pytest.raises(ValidationError):
            validate_email("")


class TestNumberValidation:
    """Tests for number validation."""

    def test_valid_positive_number(self):
        """Test valid positive number."""
        result = validate_positive_number(10.5, "test_field")
        assert result == 10.5

    def test_negative_number_fails(self):
        """Test negative number validation."""
        with pytest.raises(ValidationError):
            validate_positive_number(-5, "test_field")

    def test_number_exceeds_max(self):
        """Test number exceeding maximum."""
        with pytest.raises(ValidationError):
            validate_positive_number(150, "litres", min_val=0, max_val=100)


class TestCodeValidation:
    """Tests for code validation."""

    def test_valid_code(self):
        """Test valid code."""
        is_valid, cleaned = validate_code("01", "farmer")
        assert is_valid
        assert cleaned == "01"

    def test_code_with_lowercase(self):
        """Test code conversion to uppercase."""
        is_valid, cleaned = validate_code("abc", "farmer")
        assert is_valid
        assert cleaned == "ABC"

    def test_invalid_code_special_chars(self):
        """Test code with invalid characters."""
        with pytest.raises(ValidationError):
            validate_code("01@#", "farmer")


class TestDateValidation:
    """Tests for date validation."""

    def test_valid_date(self):
        """Test valid date."""
        is_valid, date_obj = validate_date("2024-01-15")
        assert is_valid
        assert date_obj.year == 2024
        assert date_obj.month == 1
        assert date_obj.day == 15

    def test_invalid_date_format(self):
        """Test invalid date format."""
        with pytest.raises(ValidationError):
            validate_date("15-01-2024")


class TestMilkEntryValidation:
    """Tests for milk entry validation."""

    def test_valid_milk_entry(self):
        """Test valid milk entry."""
        result = validate_milk_entry(10.5, 4.5, 8.5, 45.0)
        assert result["litres"] == 10.5
        assert result["fat"] == 4.5
        assert result["rate"] == 45.0

    def test_milk_entry_litres_too_high(self):
        """Test litres exceeding max."""
        with pytest.raises(ValidationError):
            validate_milk_entry(150)


class TestStringSanitization:
    """Tests for string sanitization."""

    def test_valid_string(self):
        """Test valid string."""
        result = sanitize_string("Normal String")
        assert result == "Normal String"

    def test_sql_injection_attempt(self):
        """Test SQL injection prevention."""
        with pytest.raises(ValidationError):
            sanitize_string("test'; DROP TABLE farmers; --")

    def test_string_too_long(self):
        """Test string length limit."""
        with pytest.raises(ValidationError):
            sanitize_string("x" * 300, max_length=255)
