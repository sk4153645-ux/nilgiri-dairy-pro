"""
Service Tests

Tests for business logic services.
"""

import pytest
from datetime import datetime
from src.services.dairy_service import DairyService
from src.services.ledger_service import LedgerService
from src.services.report_service import ReportService
from src.database.repository import FarmerRepository, CustomerRepository


class TestDairyService:
    """Tests for DairyService."""

    def test_create_farmer(self, sample_farmer_data):
        """Test farmer creation through service."""
        success, msg, farmer_id = DairyService.create_farmer(**sample_farmer_data)
        assert success
        assert farmer_id > 0

    def test_get_farmer(self, sample_farmer_data):
        """Test get farmer through service."""
        DairyService.create_farmer(**sample_farmer_data)
        success, msg, farmer = DairyService.get_farmer(sample_farmer_data["code"])
        assert success
        assert farmer["name"] == sample_farmer_data["name"]

    def test_list_farmers(self, sample_farmer_data):
        """Test list farmers."""
        DairyService.create_farmer(**sample_farmer_data)
        success, msg, farmers = DairyService.list_farmers()
        assert success
        assert len(farmers) > 0

    def test_record_milk_purchase(self, sample_farmer_data, sample_milk_entry):
        """Test milk purchase recording."""
        DairyService.create_farmer(**sample_farmer_data)
        success, msg, purchase_id = DairyService.record_milk_purchase(
            **sample_milk_entry
        )
        assert success
        assert purchase_id > 0

    def test_get_daily_collection(self, sample_farmer_data, sample_milk_entry):
        """Test get daily collection summary."""
        DairyService.create_farmer(**sample_farmer_data)
        DairyService.record_milk_purchase(**sample_milk_entry)
        success, msg, summary = DairyService.get_daily_collection(
            sample_milk_entry["date"], sample_milk_entry["shift"]
        )
        assert success
        assert "Cow" in summary

    def test_create_customer(self, sample_customer_data):
        """Test customer creation through service."""
        success, msg, customer_id = DairyService.create_customer(**sample_customer_data)
        assert success
        assert customer_id > 0


class TestLedgerService:
    """Tests for LedgerService."""

    def test_get_farmer_ledger(self, sample_farmer_data, sample_milk_entry):
        """Test get farmer ledger."""
        DairyService.create_farmer(**sample_farmer_data)
        DairyService.record_milk_purchase(**sample_milk_entry)
        success, msg, ledger = LedgerService.get_farmer_ledger(sample_farmer_data["code"])
        assert success
        assert len(ledger) > 0

    def test_get_farmer_outstanding(self, sample_farmer_data, sample_milk_entry):
        """Test get farmer outstanding amount."""
        DairyService.create_farmer(**sample_farmer_data)
        DairyService.record_milk_purchase(**sample_milk_entry)
        success, msg, outstanding = LedgerService.get_farmer_outstanding(
            sample_farmer_data["code"]
        )
        assert success
        assert outstanding > 0


class TestReportService:
    """Tests for ReportService."""

    def test_get_daily_report(self, sample_farmer_data, sample_milk_entry):
        """Test daily report generation."""
        DairyService.create_farmer(**sample_farmer_data)
        DairyService.record_milk_purchase(**sample_milk_entry)
        success, msg, report = ReportService.get_daily_report(sample_milk_entry["date"])
        assert success
        assert "morning" in report

    def test_get_outstanding_report(self, sample_farmer_data, sample_milk_entry):
        """Test outstanding report."""
        DairyService.create_farmer(**sample_farmer_data)
        DairyService.record_milk_purchase(**sample_milk_entry)
        success, msg, report = ReportService.get_outstanding_report()
        assert success
        assert isinstance(report, list)
