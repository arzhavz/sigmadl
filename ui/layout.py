# -*- coding: utf-8 -*-
from datetime import datetime

from rich import box
from rich.layout import Layout
from rich.table import Table
from rich.panel import Panel


def make_layout() -> Layout:
    layout = Layout(name="root")
    layout.split(
        Layout(name="header", size=3),
        Layout(name="body", ratio=1),
        Layout(name="footer", size=14),
    )
    return layout

class HeaderPanel:
    def __init__(self, version: str):
        self.version = version

    def __rich__(self) -> Panel:
        grid = Table.grid(expand=True)
        grid.add_column(justify="center", ratio=1)
        grid.add_column(justify="right")
        grid.add_row(
            f"[b bright_green]┌─[SIGMA-DL@{self.version}]─[~]",
            f"[b bright_black]{datetime.now().ctime().replace(':', '[blink]:[/]')}",
        )
        return Panel(
            grid,
            style="bold bright_green on black",
            border_style="bright_green",
            box=box.SQUARE,
            padding=(0, 1),
        )