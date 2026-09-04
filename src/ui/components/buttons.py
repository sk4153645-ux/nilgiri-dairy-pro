"""Custom styled buttons for UI uniformity."""

from kivy.uix.button import Button


class PrimaryButton(Button):
    """Standard primary action button (Green theme)."""

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.size_hint_y = None
        self.height = "48dp"
        self.background_color = (0.18, 0.65, 0.35, 1)
        self.font_size = "16sp"
        self.bold = True


class DangerButton(Button):
    """Destructive action button (Red theme for Delete)."""

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.size_hint_y = None
        self.height = "48dp"
        self.background_color = (0.85, 0.25, 0.20, 1)
        self.font_size = "16sp"
        self.bold = True


class SecondaryButton(Button):
    """Neutral action button (Grey/Blue theme)."""

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.size_hint_y = None
        self.height = "48dp"
        self.background_color = (0.45, 0.50, 0.55, 1)
        self.font_size = "16sp"
