"""
Pytest Configuration

Isolated test fixtures and database management.
Zero impact on production code and application features.
"""

import os
from pathlib import Path
import pytest
import sys

BASE_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(BASE_DIR))

import src.database.connection as db_conn_module
from src.database.connection import get_db
from src.database.migration import DatabaseMigration
from src.config import TestingConfig


@pytest.fixture(autouse=True)
def setup_test_db():
    """Sets up fresh tables without conflicting sample data for each test."""
    db_path = TestingConfig.DATABASE_PATH

    # Clean file if leftover
    if os.path.exists(db_path):
        try:
            os.remove(db_path)
        except Exception:
            pass

    db_conn_module._db_instance = None
    db = get_db(db_path)
    db_conn_module._db_instance = db

    # Initialize tables only (do not add sample data to prevent duplicate keys)
    DatabaseMigration.initialize(db_path)

    yield db

    db.close_all()
    db_conn_module._db_instance = None
    if os.path.exists(db_path):
        try:
            os.remove(db_path)
        except Exception:
            pass


@pytest.fixture
def sample_farmer_data():
    return {
        "code": "01",
        "name": "Test Farmer",
        "phone": "9876543210",
        "address": "Test Address",
    }


@pytest.fixture
def sample_customer_data():
    return {
        "code": "C01",
        "name": "Test Customer",
        "phone": "9876543220",
        "address": "Test Address",
    }


@pytest.fixture
def sample_milk_entry():
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
