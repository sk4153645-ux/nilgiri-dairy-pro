"""
Signup Screen

User registration screen.
"""

from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.scrollview import ScrollView
from src.ui.screens.base_screen import BaseScreen
from src.services.auth_service import AuthService


class SignupScreen(BaseScreen):
    """
    Signup screen for user registration.
    """

    def __init__(self, **kwargs):
        """
        Initialize signup screen.
        """
        super().__init__(**kwargs)
        self.build_ui()

    def build_ui(self) -> None:
        """
        Build signup screen UI.
        """
        layout = BoxLayout(orientation="vertical", padding=20, spacing=15)

        # Title
        layout.add_widget(Label(text="Create Account", font_size="18sp", size_hint_y=0.1))

        # Scrollable form
        scroll = ScrollView(size_hint_y=0.7)
        form = GridLayout(cols=1, spacing=10, size_hint_y=None)
        form.bind(minimum_height=form.setter("height"))

        self.email_input = TextInput(
            hint_text="Email",
            multiline=False,
            input_filter="mail",
            size_hint_y=None,
            height=50,
        )
        self.password_input = TextInput(
            hint_text="Password",
            password=True,
            multiline=False,
            size_hint_y=None,
            height=50,
        )
        self.dairy_name_input = TextInput(
            hint_text="Dairy Name",
            multiline=False,
            size_hint_y=None,
            height=50,
        )
        self.dairy_phone_input = TextInput(
            hint_text="Dairy Phone",
            multiline=False,
            size_hint_y=None,
            height=50,
        )

        form.add_widget(Label(text="Email:", size_hint_y=None, height=40))
        form.add_widget(self.email_input)
        form.add_widget(Label(text="Password (min 6 chars):", size_hint_y=None, height=40))
        form.add_widget(self.password_input)
        form.add_widget(Label(text="Dairy Name:", size_hint_y=None, height=40))
        form.add_widget(self.dairy_name_input)
        form.add_widget(Label(text="Dairy Phone:", size_hint_y=None, height=40))
        form.add_widget(self.dairy_phone_input)

        scroll.add_widget(form)
        layout.add_widget(scroll)

        # Buttons
        button_layout = BoxLayout(spacing=10, size_hint_y=0.2)
        signup_btn = Button(text="Sign Up", background_color=(0.2, 0.8, 0.2, 1))
        back_btn = Button(text="Back", background_color=(0.8, 0.5, 0.2, 1))

        signup_btn.bind(on_press=self.on_signup)
        back_btn.bind(on_press=self.on_back)

        button_layout.add_widget(signup_btn)
        button_layout.add_widget(back_btn)
        layout.add_widget(button_layout)

        self.add_widget(layout)

    def on_signup(self, instance) -> None:
        """
        Handle signup button press.
        """
        email = self.email_input.text.strip()
        password = self.password_input.text
        dairy_name = self.dairy_name_input.text.strip()
        dairy_phone = self.dairy_phone_input.text.strip()

        if not all([self.validate_empty(v, f) for v, f in [
            (email, "Email"),
            (password, "Password"),
            (dairy_name, "Dairy Name"),
            (dairy_phone, "Dairy Phone"),
        ]]):
            return

        success, msg = AuthService.register(email, password, dairy_name, dairy_phone)
        if success:
            self.show_success("Registration", msg)
            self.manager.current = "login"
        else:
            self.show_error("Registration Failed", msg)

    def on_back(self, instance) -> None:
        """
        Navigate back to login screen.
        """
        self.manager.current = "login"
