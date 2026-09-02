"""
Farmers Screen

Farmer management screen with add/edit/delete.
"""

from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.scrollview import ScrollView
from kivy.uix.popup import Popup
from src.ui.screens.base_screen import BaseScreen
from src.services.dairy_service import DairyService


class FarmersScreen(BaseScreen):
    """
    Farmers screen - manage farmers.
    """

    def __init__(self, **kwargs):
        """
        Initialize farmers screen.
        """
        super().__init__(**kwargs)
        self.selected_farmer = None
        self.build_ui()

    def build_ui(self) -> None:
        """
        Build farmers screen UI.
        """
        layout = BoxLayout(orientation="vertical", padding=20, spacing=10)

        # Header
        layout.add_widget(Label(text="Farmers Management", font_size="18sp", size_hint_y=0.08))

        # Form
        form = GridLayout(cols=2, spacing=10, size_hint_y=0.25)

        self.code_input = TextInput(
            hint_text="Farmer Code",
            multiline=False,
            size_hint_y=None,
            height=50,
        )
        self.name_input = TextInput(
            hint_text="Farmer Name",
            multiline=False,
            size_hint_y=None,
            height=50,
        )
        self.phone_input = TextInput(
            hint_text="Phone Number",
            multiline=False,
            size_hint_y=None,
            height=50,
        )
        self.address_input = TextInput(
            hint_text="Address",
            multiline=True,
            size_hint_y=None,
            height=80,
        )

        form.add_widget(Label(text="Code:", size_hint_x=0.3))
        form.add_widget(self.code_input)
        form.add_widget(Label(text="Name:", size_hint_x=0.3))
        form.add_widget(self.name_input)
        form.add_widget(Label(text="Phone:", size_hint_x=0.3))
        form.add_widget(self.phone_input)
        form.add_widget(Label(text="Address:", size_hint_x=0.3))
        form.add_widget(self.address_input)

        layout.add_widget(form)

        # Farmers list
        layout.add_widget(Label(text="Farmers List:", size_hint_y=0.05))
        scroll = ScrollView(size_hint_y=0.4)
        self.farmers_list = GridLayout(cols=1, spacing=10, size_hint_y=None)
        self.farmers_list.bind(minimum_height=self.farmers_list.setter("height"))
        scroll.add_widget(self.farmers_list)
        layout.add_widget(scroll)

        # Buttons
        button_layout = BoxLayout(spacing=10, size_hint_y=0.15)
        add_btn = Button(text="Add", background_color=(0.2, 0.8, 0.2, 1))
        edit_btn = Button(text="Edit", background_color=(0.2, 0.6, 0.8, 1))
        delete_btn = Button(text="Delete", background_color=(0.8, 0.2, 0.2, 1))
        back_btn = Button(text="Back", background_color=(0.8, 0.5, 0.2, 1))

        add_btn.bind(on_press=self.on_add_farmer)
        edit_btn.bind(on_press=self.on_edit_farmer)
        delete_btn.bind(on_press=self.on_delete_farmer)
        back_btn.bind(on_press=lambda x: setattr(self.manager, "current", "home"))

        button_layout.add_widget(add_btn)
        button_layout.add_widget(edit_btn)
        button_layout.add_widget(delete_btn)
        button_layout.add_widget(back_btn)
        layout.add_widget(button_layout)

        self.add_widget(layout)
        self.load_farmers()

    def load_farmers(self) -> None:
        """
        Load and display farmers list.
        """
        success, msg, farmers = DairyService.list_farmers()
        self.farmers_list.clear_widgets()

        if success and farmers:
            for farmer in farmers:
                btn = Button(
                    text=f"{farmer['code']} - {farmer['name']}",
                    size_hint_y=None,
                    height=50,
                    background_color=(0.6, 0.6, 0.6, 1),
                )
                btn.bind(
                    on_press=lambda x, f=farmer: self.select_farmer(f)
                )
                self.farmers_list.add_widget(btn)
        else:
            self.farmers_list.add_widget(
                Label(text="No farmers found", size_hint_y=None, height=50)
            )

    def select_farmer(self, farmer: dict) -> None:
        """
        Select farmer for editing.
        """
        self.selected_farmer = farmer
        self.code_input.text = farmer["code"]
        self.name_input.text = farmer["name"]
        self.phone_input.text = farmer["phone"] or ""
        self.address_input.text = farmer["address"] or ""

    def on_add_farmer(self, instance) -> None:
        """
        Add new farmer.
        """
        code = self.code_input.text.strip()
        name = self.name_input.text.strip()

        if not all([self.validate_empty(v, f) for v, f in [(code, "Code"), (name, "Name")]]):
            return

        success, msg, farmer_id = DairyService.create_farmer(
            code=code,
            name=name,
            phone=self.phone_input.text.strip(),
            address=self.address_input.text.strip(),
        )

        if success:
            self.show_success("Success", msg)
            self.code_input.text = ""
            self.name_input.text = ""
            self.load_farmers()
        else:
            self.show_error("Error", msg)

    def on_edit_farmer(self, instance) -> None:
        """
        Edit selected farmer (placeholder).
        """
        if not self.selected_farmer:
            self.show_error("Error", "Please select a farmer first")
            return
        self.show_success("Info", "Edit feature coming soon")

    def on_delete_farmer(self, instance) -> None:
        """
        Delete selected farmer (with confirmation).
        """
        if not self.selected_farmer:
            self.show_error("Error", "Please select a farmer first")
            return

        self.show_confirmation(
            "Delete Farmer",
            f"Delete {self.selected_farmer['name']}? This cannot be undone.",
            lambda: self.confirm_delete(),
        )

    def confirm_delete(self) -> None:
        """
        Confirm deletion.
        """
        self.show_success("Info", "Delete feature coming soon")
        self.selected_farmer = None
