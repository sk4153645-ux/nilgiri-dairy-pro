"""Modal dialog and popup helpers."""

from typing import Callable, Optional
from kivy.uix.popup import Popup
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button


def show_alert(title: str, message: str, on_dismiss_callback: Optional[Callable] = None):
    """Displays a simple alert popup."""
    layout = BoxLayout(orientation="vertical", padding=15, spacing=10)
    layout.add_widget(Label(text=message, halign="center", valign="middle"))

    btn = Button(text="OK", size_hint_y=None, height="44dp")
    layout.add_widget(btn)

    popup = Popup(title=title, content=layout, size_hint=(0.8, 0.4), auto_dismiss=False)
    btn.bind(on_release=popup.dismiss)
    if on_dismiss_callback:
        popup.bind(on_dismiss=lambda x: on_dismiss_callback())
    popup.open()


def show_confirm(title: str, message: str, on_confirm: Callable, on_cancel: Optional[Callable] = None):
    """Displays a confirmation popup with YES/NO actions."""
    layout = BoxLayout(orientation="vertical", padding=15, spacing=10)
    layout.add_widget(Label(text=message, halign="center", valign="middle"))

    btn_box = BoxLayout(size_hint_y=None, height="44dp", spacing=10)
    yes_btn = Button(text="Confirm", background_color=(0.18, 0.65, 0.35, 1))
    no_btn = Button(text="Cancel", background_color=(0.85, 0.25, 0.20, 1))

    btn_box.add_widget(yes_btn)
    btn_box.add_widget(no_btn)
    layout.add_widget(btn_box)

    popup = Popup(title=title, content=layout, size_hint=(0.85, 0.45), auto_dismiss=False)

    def _on_yes(_):
        popup.dismiss()
        on_confirm()

    def _on_no(_):
        popup.dismiss()
        if on_cancel:
            on_cancel()

    yes_btn.bind(on_release=_on_yes)
    no_btn.bind(on_release=_on_no)
    popup.open()


def show_loading(title: str = "Processing...") -> Popup:
    """Returns a dismissible loading modal."""
    layout = BoxLayout(orientation="vertical", padding=20)
    layout.add_widget(Label(text="Please wait..."))
    popup = Popup(title=title, content=layout, size_hint=(0.6, 0.3), auto_dismiss=False)
    popup.open()
    return popup
