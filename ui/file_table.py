# -*- coding: utf-8 -*-
import os

from rich import box
from rich.table import Table

from core.utils import human_readable_size


def create_log_table() -> Table:
    table = Table.grid(padding=1)
    table.add_column("Time", style="bright_black", no_wrap=True)
    table.add_column("Level", style="bright_green", no_wrap=True)
    table.add_column("Message", style="bright_white")
    return table

def create_file_table(files: list, folder: str, title: str = "Downloaded Files") -> Table:
    file_table = Table(title=f"[b bright_green]{title}", box=box.SQUARE)
    file_table.add_column("File Name", style="bright_green")
    file_table.add_column("Size", style="bright_white", justify="right")
    for f in files:
        file_path = os.path.join(folder, f)
        size_bytes = os.path.getsize(file_path)
        file_table.add_row(f, human_readable_size(size_bytes))
    return file_table
