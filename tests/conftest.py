"""
Pytest Configuration

Setup for testing with fixtures, mocking, and database reset.
"""

import pytest
import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.database.connection import get_db
from src.database.migration import DatabaseMigration
from src.config import TestingConfig


@pytest.fixture(autouse=True)
def setup_test_db():
    """
    Auto-run before EVERY test:
    Initializes a fresh test database with tables and sample data.
    """
    db_path = TestingConfig.DATABASE_PATH
    db = get_db(db_path)
    
    # Run migration methods directly
    try:
        DatabaseMigration.initialize(db_path)
    except AttributeError:
        # Fallback if instance-based
        migration = DatabaseMigration(db)
        migration.run_migrations()

    try:
        DatabaseMigration.add_sample_data(db_path)
    except (AttributeError, Exception):
        pass

    yield db

    # Teardown
    db.close_all()


@pytest.fixture
def sample_farmer_data():
    """Sample farmer data for testing."""
    return {
        "code": "01",
        "name": "Test Farmer",
        "phone": "9876543210",
        "address": "Test Address",
    }


@pytest.fixture
def sample_customer_data():
    """Sample customer data for testing."""
    return {
        "code": "C01",
        "name": "Test Customer",
        "phone": "9876543220",
        "address": "Test Address",
    }


@pytest.fixture
def sample_milk_entry():
    """Sample milk entry data for testing."""
    return {
        "date": "2024-01-01",
        "shift": "Morning",
        "farmer_code": "01",
        "milk_type": "Cow",
        "litres": 10.5,
        "fat": 4.5,
        "snf": 8.5,
        "rate": 45.0,
    }
