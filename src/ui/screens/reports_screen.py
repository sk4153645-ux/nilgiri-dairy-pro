"""
Reports Screen

Reports and analytics screen.
"""

from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from src.ui.screens.base_screen import BaseScreen


class ReportsScreen(BaseScreen):
    """
    Reports screen - view reports and analytics.
    """

    def __init__(self, **kwargs):
        """
        Initialize reports screen.
        """
        super().__init__(**kwargs)
        self.build_ui()

    def build_ui(self) -> None:
        """
        Build reports screen UI.
        """
        layout = BoxLayout(orientation="vertical", padding=20, spacing=15)

        layout.add_widget(Label(text="Reports & Analytics", font_size="18sp"))
        layout.add_widget(Label(text="Feature coming soon...", font_size="16sp"))

        back_btn = Button(text="Back", background_color=(0.8, 0.5, 0.2, 1), size_hint_y=0.2)
        back_btn.bind(on_press=lambda x: setattr(self.manager, "current", "home"))
        layout.add_widget(back_btn)

        self.add_widget(layout)
