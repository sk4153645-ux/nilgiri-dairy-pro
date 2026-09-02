"""
Settings Screen

Application settings screen.
"""

from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from src.ui.screens.base_screen import BaseScreen
from src.services.backup_service import BackupService


class SettingsScreen(BaseScreen):
    """
    Settings screen - application settings.
    """

    def __init__(self, **kwargs):
        """
        Initialize settings screen.
        """
        super().__init__(**kwargs)
        self.build_ui()

    def build_ui(self) -> None:
        """
        Build settings screen UI.
        """
        layout = BoxLayout(orientation="vertical", padding=20, spacing=15)

        layout.add_widget(Label(text="Settings", font_size="18sp", size_hint_y=0.1))

        # Settings buttons
        button_layout = BoxLayout(orientation="vertical", spacing=10, size_hint_y=0.7)

        backup_btn = Button(
            text="Create Backup",
            background_color=(0.2, 0.8, 0.2, 1),
            size_hint_y=None,
            height=60,
        )
        restore_btn = Button(
            text="Restore Backup",
            background_color=(0.2, 0.6, 0.8, 1),
            size_hint_y=None,
            height=60,
        )
        about_btn = Button(
            text="About",
            background_color=(0.6, 0.6, 0.6, 1),
            size_hint_y=None,
            height=60,
        )

        backup_btn.bind(on_press=self.on_backup)
        restore_btn.bind(on_press=self.on_restore)
        about_btn.bind(on_press=self.on_about)

        button_layout.add_widget(backup_btn)
        button_layout.add_widget(restore_btn)
        button_layout.add_widget(about_btn)
        layout.add_widget(button_layout)

        # Back button
        back_btn = Button(text="Back", background_color=(0.8, 0.5, 0.2, 1), size_hint_y=0.2)
        back_btn.bind(on_press=lambda x: setattr(self.manager, "current", "home"))
        layout.add_widget(back_btn)

        self.add_widget(layout)

    def on_backup(self, instance) -> None:
        """
        Create backup.
        """
        success, msg, path = BackupService.create_backup()
        if success:
            self.show_success("Backup", msg)
        else:
            self.show_error("Backup Failed", msg)

    def on_restore(self, instance) -> None:
        """
        Restore backup (placeholder).
        """
        self.show_success("Info", "Restore feature coming soon")

    def on_about(self, instance) -> None:
        """
        Show about information.
        """
        self.show_success(
            "About",
            "Nilgiri Dairy Pro v1.0.0\n" 
            "Production-grade Dairy Management System\n"
            "© 2024 Nilgiri Dairy"
        )
