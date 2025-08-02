# -*- coding: utf-8 -*-
from rich.layout import Layout

def make_layout() -> Layout:
    """Create the layout for the application."""
    layout = Layout(name="root")
    layout.split(
        Layout(name="header", size=3),
        Layout(name="body", ratio=1),
        Layout(name="footer", size=14),
    )
    return layout