"""
Home Screen

Main dashboard screen.
"""

from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.popup import Popup
from src.ui.screens.base_screen import BaseScreen


class HomeScreen(BaseScreen):
    """
    Home screen - main dashboard.
    """

    def __init__(self, **kwargs):
        """
        Initialize home screen.
        """
        super().__init__(**kwargs)
        self.build_ui()

    def build_ui(self) -> None:
        """
        Build home screen UI with menu buttons.
        """
        layout = BoxLayout(orientation="vertical", padding=20, spacing=15)

        # Header
        layout.add_widget(Label(text="Nilgiri Dairy Pro", font_size="24sp", size_hint_y=0.1))
        layout.add_widget(Label(text="Dashboard", font_size="18sp", size_hint_y=0.08))

        # Menu grid
        menu = GridLayout(cols=2, spacing=15, size_hint_y=0.7)

        buttons = [
            ("Buy Milk", "buy_milk", (0.2, 0.8, 0.2, 1)),
            ("Farmers", "farmers", (0.2, 0.6, 0.8, 1)),
            ("Customers", "customers", (0.8, 0.6, 0.2, 1)),
            ("Collection", "collection_list", (0.6, 0.2, 0.8, 1)),
            ("Daily Entry", "daily_entry", (0.2, 0.8, 0.6, 1)),
            ("Scan Register", "scan_register", (0.8, 0.8, 0.2, 1)),
            ("Ledger", "ledger", (0.8, 0.2, 0.2, 1)),
            ("Reports", "reports", (0.2, 0.2, 0.8, 1)),
        ]

        for text, screen, color in buttons:
            btn = Button(text=text, background_color=color, font_size="14sp")
            btn.bind(
                on_press=lambda x, s=screen: setattr(self.manager, "current", s)
            )
            menu.add_widget(btn)

        layout.add_widget(menu)

        # Bottom buttons
        bottom_layout = BoxLayout(spacing=10, size_hint_y=0.12)
        settings_btn = Button(text="Settings", background_color=(0.6, 0.6, 0.6, 1))
        logout_btn = Button(text="Logout", background_color=(0.8, 0.2, 0.2, 1))

        settings_btn.bind(
            on_press=lambda x: setattr(self.manager, "current", "settings")
        )
        logout_btn.bind(on_press=self.on_logout)

        bottom_layout.add_widget(settings_btn)
        bottom_layout.add_widget(logout_btn)
        layout.add_widget(bottom_layout)

        self.add_widget(layout)

    def on_logout(self, instance) -> None:
        """
        Handle logout.
        """
        self.show_confirmation(
            "Logout",
            "Are you sure you want to logout?",
            lambda: setattr(self.manager, "current", "login"),
        )
