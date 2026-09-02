"""
Buy Milk Screen

Milk purchase recording screen.
"""

from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.spinner import Spinner
from src.ui.screens.base_screen import BaseScreen
from src.services.dairy_service import DairyService
from datetime import datetime


class BuyMilkScreen(BaseScreen):
    """
    Buy milk screen - record milk purchases from farmers.
    """

    def __init__(self, **kwargs):
        """
        Initialize buy milk screen.
        """
        super().__init__(**kwargs)
        self.build_ui()

    def build_ui(self) -> None:
        """
        Build buy milk screen UI.
        """
        layout = BoxLayout(orientation="vertical", padding=20, spacing=10)

        # Header
        layout.add_widget(Label(text="Record Milk Purchase", font_size="18sp", size_hint_y=0.08))

        # Form
        form = GridLayout(cols=2, spacing=10, size_hint_y=0.6)

        self.farmer_input = TextInput(
            hint_text="Farmer Code",
            multiline=False,
            size_hint_y=None,
            height=50,
        )
        self.date_input = TextInput(
            hint_text="Date (YYYY-MM-DD)",
            text=datetime.now().strftime("%Y-%m-%d"),
            multiline=False,
            size_hint_y=None,
            height=50,
        )
        self.shift_spinner = Spinner(
            text="Morning",
            values=("Morning", "Evening"),
            size_hint_y=None,
            height=50,
        )
        self.milk_type_spinner = Spinner(
            text="Cow",
            values=("Cow", "Buffalo"),
            size_hint_y=None,
            height=50,
        )
        self.litres_input = TextInput(
            hint_text="Litres",
            input_filter="float",
            multiline=False,
            size_hint_y=None,
            height=50,
        )
        self.fat_input = TextInput(
            hint_text="Fat %",
            input_filter="float",
            multiline=False,
            size_hint_y=None,
            height=50,
        )
        self.rate_input = TextInput(
            hint_text="Rate/L",
            input_filter="float",
            multiline=False,
            size_hint_y=None,
            height=50,
        )

        form.add_widget(Label(text="Farmer Code:", size_hint_x=0.3))
        form.add_widget(self.farmer_input)
        form.add_widget(Label(text="Date:", size_hint_x=0.3))
        form.add_widget(self.date_input)
        form.add_widget(Label(text="Shift:", size_hint_x=0.3))
        form.add_widget(self.shift_spinner)
        form.add_widget(Label(text="Milk Type:", size_hint_x=0.3))
        form.add_widget(self.milk_type_spinner)
        form.add_widget(Label(text="Litres:", size_hint_x=0.3))
        form.add_widget(self.litres_input)
        form.add_widget(Label(text="Fat %:", size_hint_x=0.3))
        form.add_widget(self.fat_input)
        form.add_widget(Label(text="Rate/L:", size_hint_x=0.3))
        form.add_widget(self.rate_input)

        layout.add_widget(form)

        # Buttons
        button_layout = BoxLayout(spacing=10, size_hint_y=0.12)
        save_btn = Button(text="Save", background_color=(0.2, 0.8, 0.2, 1))
        clear_btn = Button(text="Clear", background_color=(0.8, 0.8, 0.2, 1))
        back_btn = Button(text="Back", background_color=(0.8, 0.5, 0.2, 1))

        save_btn.bind(on_press=self.on_save)
        clear_btn.bind(on_press=self.on_clear)
        back_btn.bind(on_press=lambda x: setattr(self.manager, "current", "home"))

        button_layout.add_widget(save_btn)
        button_layout.add_widget(clear_btn)
        button_layout.add_widget(back_btn)
        layout.add_widget(button_layout)

        self.add_widget(layout)

    def on_save(self, instance) -> None:
        """
        Handle save button press.
        """
        farmer_code = self.farmer_input.text.strip()
        litres = self.litres_input.text.strip()
        rate = self.rate_input.text.strip()

        if not all([self.validate_empty(v, f) for v, f in [
            (farmer_code, "Farmer Code"),
            (litres, "Litres"),
            (rate, "Rate"),
        ]]):
            return

        try:
            success, msg, purchase_id = DairyService.record_milk_purchase(
                date=self.date_input.text,
                shift=self.shift_spinner.text,
                farmer_code=farmer_code,
                milk_type=self.milk_type_spinner.text,
                litres=float(litres),
                fat=float(self.fat_input.text) if self.fat_input.text else 0,
                rate=float(rate),
            )
            if success:
                self.show_success("Success", msg)
                self.on_clear(None)
            else:
                self.show_error("Error", msg)
        except ValueError:
            self.show_error("Error", "Please enter valid numbers")

    def on_clear(self, instance) -> None:
        """
        Clear form.
        """
        self.clear_form({
            "farmer": self.farmer_input,
            "litres": self.litres_input,
            "fat": self.fat_input,
            "rate": self.rate_input,
        })
        self.date_input.text = datetime.now().strftime("%Y-%m-%d")
        self.shift_spinner.text = "Morning"
        self.milk_type_spinner.text = "Cow"
