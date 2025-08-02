# -*- coding: utf-8 -*-
from datetime import datetime
from rich.table import Table
from rich.panel import Panel
from rich import box
from constants import VERSION

class Header:
    """Header class to display the application header with version and current time."""
    def __rich__(self) -> Panel:
        grid = Table.grid(expand=True)
        grid.add_column(justify="center", ratio=1)
        grid.add_column(justify="right")
        grid.add_row(
            f"[b bright_green]┌─[SIGMA-DL@{VERSION}]─[~]",
            f"[b bright_black]{datetime.now().ctime().replace(':', '[blink]:[/]')}",
        )
        return Panel(
            grid,
            style="bold bright_green on black",
            border_style="bright_green",
            box=box.SQUARE,
            padding=(0, 1),
        )