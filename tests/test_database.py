"""
Database Tests

Tests for database operations and repositories.
"""

import pytest
from src.database.connection import get_db
from src.database.repository import (
    FarmerRepository,
    CustomerRepository,
    MilkPurchaseRepository,
)
from src.core.exceptions import DuplicateError, NotFoundError


class TestFarmerRepository:
    """Tests for FarmerRepository."""

    def test_create_farmer(self, sample_farmer_data):
        """Test farmer creation."""
        farmer_id = FarmerRepository.create(**sample_farmer_data)
        assert farmer_id > 0

    def test_get_farmer(self, sample_farmer_data):
        """Test get farmer by code."""
        FarmerRepository.create(**sample_farmer_data)
        farmer = FarmerRepository.get_by_code(sample_farmer_data["code"])
        assert farmer is not None
        assert farmer["name"] == sample_farmer_data["name"]

    def test_duplicate_farmer_code(self, sample_farmer_data):
        """Test duplicate farmer code."""
        FarmerRepository.create(**sample_farmer_data)
        with pytest.raises(DuplicateError):
            FarmerRepository.create(**sample_farmer_data)

    def test_get_all_farmers(self, sample_farmer_data):
        """Test get all farmers."""
        FarmerRepository.create(**sample_farmer_data)
        farmers = FarmerRepository.get_all()
        assert len(farmers) > 0


class TestCustomerRepository:
    """Tests for CustomerRepository."""

    def test_create_customer(self, sample_customer_data):
        """Test customer creation."""
        customer_id = CustomerRepository.create(**sample_customer_data)
        assert customer_id > 0

    def test_get_customer(self, sample_customer_data):
        """Test get customer by code."""
        CustomerRepository.create(**sample_customer_data)
        customer = CustomerRepository.get_by_code(sample_customer_data["code"])
        assert customer is not None
        assert customer["name"] == sample_customer_data["name"]


class TestMilkPurchaseRepository:
    """Test cases for MilkPurchaseRepository."""

    def test_create_milk_purchase(self, sample_farmer_data, sample_milk_entry):
        """Test milk purchase creation."""
        FarmerRepository.create(**sample_farmer_data)
        data = dict(sample_milk_entry)
        if "total_amount" not in data:
            data["total_amount"] = round(data["litres"] * data["rate"], 2)
        purchase_id = MilkPurchaseRepository.create(**data)
        assert purchase_id > 0

    def test_get_by_date_shift(self, sample_farmer_data, sample_milk_entry):
        """Test get purchases by date and shift."""
        FarmerRepository.create(**sample_farmer_data)
        data = dict(sample_milk_entry)
        if "total_amount" not in data:
            data["total_amount"] = round(data["litres"] * data["rate"], 2)
        MilkPurchaseRepository.create(**data)
        purchases = MilkPurchaseRepository.get_by_date_shift(
            sample_milk_entry["date"], sample_milk_entry["shift"]
        )
        assert len(purchases) > 0

    def test_delete_milk_purchase(self, sample_farmer_data, sample_milk_entry):
        """Test milk purchase deletion."""
        FarmerRepository.create(**sample_farmer_data)
        data = dict(sample_milk_entry)
        if "total_amount" not in data:
            data["total_amount"] = round(data["litres"] * data["rate"], 2)
        purchase_id = MilkPurchaseRepository.create(**data)
        MilkPurchaseRepository.delete(purchase_id)
        purchases = MilkPurchaseRepository.get_by_date_shift(
            sample_milk_entry["date"], sample_milk_entry["shift"]
        )
        assert len(purchases) == 0
