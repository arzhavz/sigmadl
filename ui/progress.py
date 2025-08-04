# -*- coding: utf-8 -*-
from rich.progress import (
    Progress, 
    SpinnerColumn, 
    BarColumn, 
    TextColumn, 
    TimeElapsedColumn, 
    TimeRemainingColumn
)  

from core.utils import human_readable_size


class HumanSizeColumn(TextColumn):
    def __init__(self):
        super().__init__("{task.completed}") 
    def render(self, task):
        completed = task.completed or 0
        total = task.total or 0
        return f"[progress.completed][bright_black]{human_readable_size(int(completed))} / {human_readable_size(int(total))}[/]"

def create_progress() -> Progress:
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