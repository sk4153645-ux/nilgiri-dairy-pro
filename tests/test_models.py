"""
Model Tests

Tests for data models and validation.
"""

import pytest
from src.models.farmer import Farmer
from src.models.customer import Customer
from src.models.milk_entry import MilkEntry
from src.models.payment import Payment


class TestFarmerModel:
    """Tests for Farmer model."""

    def test_farmer_creation(self, sample_farmer_data):
        """Test farmer creation."""
        farmer = Farmer(**sample_farmer_data)
        assert farmer.code == "01"
        assert farmer.name == "Test Farmer"
        assert farmer.phone == "9876543210"

    def test_farmer_validation_success(self, sample_farmer_data):
        """Test valid farmer validation."""
        farmer = Farmer(**sample_farmer_data)
        is_valid, error = farmer.validate()
        assert is_valid
        assert error == ""

    def test_farmer_missing_name(self, sample_farmer_data):
        """Test farmer without name."""
        sample_farmer_data["name"] = ""
        farmer = Farmer(**sample_farmer_data)
        is_valid, error = farmer.validate()
        assert not is_valid
        assert "name" in error.lower()

    def test_farmer_fixed_rate(self, sample_farmer_data):
        """Test farmer with fixed rate."""
        sample_farmer_data["rate_type"] = "fixed"
        sample_farmer_data["fixed_rate"] = 50.0
        farmer = Farmer(**sample_farmer_data)
        is_valid, error = farmer.validate()
        assert is_valid
        assert farmer.get_rate(40.0) == 50.0

    def test_farmer_variable_rate(self, sample_farmer_data):
        """Test farmer with variable rate."""
        farmer = Farmer(**sample_farmer_data)
        rate = farmer.get_rate(40.0)
        assert rate == 40.0


class TestCustomerModel:
    """Tests for Customer model."""

    def test_customer_creation(self, sample_customer_data):
        """Test customer creation."""
        customer = Customer(**sample_customer_data)
        assert customer.code == "C01"
        assert customer.name == "Test Customer"

    def test_customer_validation_success(self, sample_customer_data):
        """Test valid customer validation."""
        customer = Customer(**sample_customer_data)
        is_valid, error = customer.validate()
        assert is_valid


class TestMilkEntryModel:
    """Tests for MilkEntry model."""

    def test_milk_entry_creation(self, sample_milk_entry):
        """Test milk entry creation."""
        entry = MilkEntry(**sample_milk_entry)
        assert entry.litres == 10.5
        assert entry.milk_type == "Cow"

    def test_milk_entry_validation_success(self, sample_milk_entry):
        """Test valid milk entry validation."""
        entry = MilkEntry(**sample_milk_entry)
        is_valid, error = entry.validate()
        assert is_valid

    def test_milk_entry_calculate_total(self, sample_milk_entry):
        """Test total amount calculation."""
        entry = MilkEntry(**sample_milk_entry)
        total = entry.calculate_total()
        assert total == pytest.approx(10.5 * 45.0, 0.01)

    def test_milk_entry_invalid_milk_type(self, sample_milk_entry):
        """Test invalid milk type."""
        sample_milk_entry["milk_type"] = "Goat"
        entry = MilkEntry(**sample_milk_entry)
        is_valid, error = entry.validate()
        assert not is_valid


class TestPaymentModel:
    """Tests for Payment model."""

    def test_payment_creation(self):
        """Test payment creation."""
        payment = Payment(
            date="2024-01-01",
            entity_code="01",
            amount=500.0,
            payment_mode="Cash",
        )
        assert payment.amount == 500.0
        assert payment.payment_mode == "Cash"

    def test_payment_validation_success(self):
        """Test valid payment validation."""
        payment = Payment(
            date="2024-01-01",
            entity_code="01",
            amount=500.0,
            payment_mode="Cash",
        )
        is_valid, error = payment.validate()
        assert is_valid
