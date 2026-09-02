"""
UI Module - Kivy Screens

All application screens and UI components.
"""

from src.ui.screens.login_screen import LoginScreen
from src.ui.screens.signup_screen import SignupScreen
from src.ui.screens.home_screen import HomeScreen
from src.ui.screens.farmers_screen import FarmersScreen
from src.ui.screens.customers_screen import CustomersScreen
from src.ui.screens.buy_milk_screen import BuyMilkScreen
from src.ui.screens.collection_list_screen import CollectionListScreen
from src.ui.screens.daily_entry_screen import DailyEntryScreen
from src.ui.screens.scan_register_screen import ScanRegisterScreen
from src.ui.screens.ledger_screen import LedgerScreen
from src.ui.screens.reports_screen import ReportsScreen
from src.ui.screens.settings_screen import SettingsScreen

__all__ = [
    "LoginScreen",
    "SignupScreen",
    "HomeScreen",
    "FarmersScreen",
    "CustomersScreen",
    "BuyMilkScreen",
    "CollectionListScreen",
    "DailyEntryScreen",
    "ScanRegisterScreen",
    "LedgerScreen",
    "ReportsScreen",
    "SettingsScreen",
]
