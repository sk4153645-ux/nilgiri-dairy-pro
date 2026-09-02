"""
Main Application Entry Point

Initializes and runs the Kivy application.
"""

from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label

from src.config import Config
from src.database.migration import DatabaseMigration
from src.logger import setup_logger
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

logger = setup_logger(__name__)


class NilgiriDairyApp(App):
    """
    Main Kivy application class.
    """

    def build(self):
        """
        Build and return the app.
        """
        # Initialize database
        try:
            DatabaseMigration.initialize(Config.DATABASE_PATH)
            if Config.DATABASE_RESET_ON_START:
                DatabaseMigration.add_sample_data(Config.DATABASE_PATH)
            logger.info("Database initialized successfully")
        except Exception as e:
            logger.error(f"Failed to initialize database: {e}")
            return BoxLayout(
                orientation="vertical",
                padding=20,
                spacing=15,
            )

        # Create screen manager
        sm = ScreenManager()

        # Add all screens
        sm.add_widget(LoginScreen(name="login"))
        sm.add_widget(SignupScreen(name="signup"))
        sm.add_widget(HomeScreen(name="home"))
        sm.add_widget(FarmersScreen(name="farmers"))
        sm.add_widget(CustomersScreen(name="customers"))
        sm.add_widget(BuyMilkScreen(name="buy_milk"))
        sm.add_widget(CollectionListScreen(name="collection_list"))
        sm.add_widget(DailyEntryScreen(name="daily_entry"))
        sm.add_widget(ScanRegisterScreen(name="scan_register"))
        sm.add_widget(LedgerScreen(name="ledger"))
        sm.add_widget(ReportsScreen(name="reports"))
        sm.add_widget(SettingsScreen(name="settings"))

        # Set default screen
        sm.current = "login"

        logger.info("Application started")
        return sm


def main():
    """
    Entry point for application.
    """
    app = NilgiriDairyApp()
    app.title = Config.APP_NAME
    app.run()


if __name__ == "__main__":
    main()
