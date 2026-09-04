"""Reusable Header component for Kivy screens."""

from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.properties import StringProperty, ObjectProperty


class AppHeader(BoxLayout):
    title = StringProperty("Nilgiri Dairy Pro")
    on_back = ObjectProperty(None)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.orientation = "horizontal"
        self.size_hint_y = None
        self.height = "56dp"
        self.padding = ["12dp", "8dp"]
        self.spacing = "10dp"

        if self.on_back:
            back_btn = Button(
                text="< Back",
                size_hint_x=None,
                width="80dp",
                background_color=(0.2, 0.4, 0.6, 1),
            )
            back_btn.bind(on_release=lambda x: self.on_back())
            self.add_widget(back_btn)

        title_lbl = Label(
            text=self.title,
            font_size="20sp",
            bold=True,
            halign="left",
            valign="middle",
        )
        title_lbl.bind(size=title_lbl.setter("text_size"))
        self.add_widget(title_lbl)
