"""
Login Screen

User authentication screen.
"""

from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from src.ui.screens.base_screen import BaseScreen
from src.services.auth_service import AuthService


class LoginScreen(BaseScreen):
    """
    Login screen for user authentication.
    """

    def __init__(self, **kwargs):
        """
        Initialize login screen.
        """
        super().__init__(**kwargs)
        self.build_ui()

    def build_ui(self) -> None:
        """
        Build login screen UI.
        """
        layout = BoxLayout(orientation="vertical", padding=20, spacing=15)

        # Title
        layout.add_widget(Label(text="Nilgiri Dairy Pro", font_size="24sp", size_hint_y=0.2))
        layout.add_widget(Label(text="Login", font_size="18sp", size_hint_y=0.1))

        # Form
        form = GridLayout(cols=1, spacing=10, size_hint_y=0.4)

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

        form.add_widget(Label(text="Email:", size_hint_y=None, height=40))
        form.add_widget(self.email_input)
        form.add_widget(Label(text="Password:", size_hint_y=None, height=40))
        form.add_widget(self.password_input)

        layout.add_widget(form)

        # Buttons
        button_layout = BoxLayout(spacing=10, size_hint_y=0.2)
        login_btn = Button(text="Login", background_color=(0.2, 0.8, 0.2, 1))
        signup_btn = Button(text="Sign Up", background_color=(0.2, 0.6, 0.8, 1))

        login_btn.bind(on_press=self.on_login)
        signup_btn.bind(on_press=self.on_signup)

        button_layout.add_widget(login_btn)
        button_layout.add_widget(signup_btn)
        layout.add_widget(button_layout)

        self.add_widget(layout)

    def on_login(self, instance) -> None:
        """
        Handle login button press.
        """
        email = self.email_input.text.strip()
        password = self.password_input.text

        if not self.validate_empty(email, "Email"):
            return
        if not self.validate_empty(password, "Password"):
            return

        success, msg, user = AuthService.login(email, password)
        if success:
            self.show_success("Login", msg)
            # Navigate to home screen
            self.manager.current = "home"
        else:
            self.show_error("Login Failed", msg)

    def on_signup(self, instance) -> None:
        """
        Navigate to signup screen.
        """
        self.manager.current = "signup"
