# -*- coding: utf-8 -*-
from rich.progress import Progress, SpinnerColumn, BarColumn, TextColumn, TimeElapsedColumn, TimeRemainingColumn
from rich.text import Text
from .components import HumanSizeColumn

def create_progress() -> Progress:
    """Create a progress bar with custom columns."""
    return Progress(
        SpinnerColumn(style="bold bright_green", spinner_name="aesthetic"),
        BarColumn(bar_width=None, style="bright_green", complete_style="green"),
        TextColumn("[progress.description][bright_green]{task.description}[/]", style="bold bright_green"),
        TextColumn("[progress.percentage][bright_white]{task.percentage:>3.0f}%[/]"),
        HumanSizeColumn(),
        TimeElapsedColumn(),
        TimeRemainingColumn(),
        expand=True,
    )