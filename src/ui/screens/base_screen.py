"""
Base Screen Class

Provides common functionality for all screens.
"""

from kivy.screen import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.popup import Popup
from kivy.uix.textinput import TextInput
from src.logger import setup_logger

logger = setup_logger(__name__)


class BaseScreen(Screen):
    """
    Base screen class with common functionality.

    Provides:
        - Error handling
        - User confirmations
        - Loading indicators
        - Logging
    """

    def __init__(self, **kwargs):
        """
        Initialize base screen.
        """
        super().__init__(**kwargs)
        self.logger = logger

    def show_error(self, title: str, message: str) -> None:
        """
        Show error popup.

        Args:
            title: Popup title
            message: Error message
        """
        self.logger.warning(f"{title}: {message}")
        self._show_popup(title, message, "Error")

    def show_success(self, title: str, message: str) -> None:
        """
        Show success popup.

        Args:
            title: Popup title
            message: Success message
        """
        self.logger.info(f"{title}: {message}")
        self._show_popup(title, message, "Success")

    def show_confirmation(
        self, title: str, message: str, callback_yes, callback_no=None
    ) -> None:
        """
        Show confirmation dialog.

        Args:
            title: Dialog title
            message: Confirmation message
            callback_yes: Callback if user clicks Yes
            callback_no: Callback if user clicks No (optional)
        """
        content = BoxLayout(orientation="vertical", padding=10, spacing=10)
        content.add_widget(Label(text=message, size_hint_y=0.7))

        button_layout = BoxLayout(size_hint_y=0.3, spacing=10)
        yes_btn = Button(text="Yes", background_color=(0.2, 0.8, 0.2, 1))
        no_btn = Button(text="No", background_color=(0.8, 0.2, 0.2, 1))

        popup = Popup(title=title, content=content, size_hint=(0.9, 0.6))

        def on_yes(instance):
            popup.dismiss()
            callback_yes()

        def on_no(instance):
            popup.dismiss()
            if callback_no:
                callback_no()

        yes_btn.bind(on_press=on_yes)
        no_btn.bind(on_press=on_no)

        button_layout.add_widget(yes_btn)
        button_layout.add_widget(no_btn)
        content.add_widget(button_layout)
        popup.open()

    def _show_popup(self, title: str, message: str, popup_type: str) -> None:
        """
        Show generic popup.

        Args:
            title: Popup title
            message: Popup message
            popup_type: Type of popup (Error, Success, Info)
        """
        content = BoxLayout(orientation="vertical", padding=10, spacing=10)
        content.add_widget(Label(text=message, size_hint_y=0.8))

        close_btn = Button(text="Close", size_hint_y=0.2)
        popup = Popup(
            title=title,
            content=content,
            size_hint=(0.9, 0.6),
        )
        close_btn.bind(on_press=popup.dismiss)
        content.add_widget(close_btn)
        popup.open()

    def validate_empty(self, value: str, field_name: str) -> bool:
        """
        Validate field is not empty.

        Args:
            value: Field value
            field_name: Field name for error message

        Returns:
            True if valid, False otherwise
        """
        if not value or not value.strip():
            self.show_error("Validation Error", f"{field_name} is required")
            return False
        return True

    def clear_form(self, form_fields: dict) -> None:
        """
        Clear form fields.

        Args:
            form_fields: Dictionary of field_name: widget
        """
        for widget in form_fields.values():
            if isinstance(widget, TextInput):
                widget.text = ""
