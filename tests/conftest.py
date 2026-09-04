"""
Pytest Configuration

Isolated test fixtures and database management.
Zero impact on production code and application features.
"""

import os
from pathlib import Path
import pytest
import sys

# Ensure project root is in sys.path
BASE_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(BASE_DIR))

import src.database.connection as db_conn_module
from src.database.connection import get_db
from src.database.migration import DatabaseMigration
from src.config import TestingConfig


@pytest.fixture(autouse=True)
def setup_test_db():
    """
    Sets up an isolated database for tests and cleans up afterwards.
    Ensures singleton connection points directly to the test schema.
    """
    db_path = TestingConfig.DATABASE_PATH

    # Reset singleton and point to test db
    db_conn_module._db_instance = None
    db = get_db(db_path)
    db_conn_module._db_instance = db

    # Run schema creation on test database
    try:
        DatabaseMigration.initialize(db_path)
    except Exception:
        pass

    try:
        DatabaseMigration.add_sample_data(db_path)
    except Exception:
        pass

    yield db

    # Teardown connection
    db.close_all()
    db_conn_module._db_instance = None


@pytest.fixture
def sample_farmer_data():
    """Sample farmer fixture for test isolation."""
    return {
        "code": "01",
        "name": "Test Farmer",
        "phone": "9876543210",
        "address": "Test Address",
    }


@pytest.fixture
def sample_customer_data():
    """Sample customer fixture for test isolation."""
    return {
        "code": "C01",
        "name": "Test Customer",
        "phone": "9876543220",
        "address": "Test Address",
    }


@pytest.fixture
def sample_milk_entry():
    """Sample milk entry fixture for test isolation."""
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
