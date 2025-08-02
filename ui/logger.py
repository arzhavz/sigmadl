# -*- coding: utf-8 -*-
import logging
from datetime import datetime
from rich.panel import Panel
from rich import box

class UILogger(logging.Handler):
    """A custom logging handler that formats log messages for display in a Rich UI."""
    def __init__(self, table, layout):
        super().__init__()
        self.table = table
        self.layout = layout

    def emit(self, record):
        """Emit a log record to the Rich UI."""
        msg = self.format(record)
        time_str = f"[bright_black]{datetime.now().strftime('%H:%M:%S')}[/]"
        level = record.levelname
        color = {
            "INFO": "bright_green",
            "WARNING": "yellow",
            "ERROR": "bright_red",
            "CRITICAL": "bold bright_red",
            "DEBUG": "cyan"
        }.get(level, "bright_green")
        self.table.add_row(time_str, f"[{color}]{level}[/]", f"[bright_white]{msg}[/]")
        self.layout["body"].update(
            Panel(
                self.table,
                title="[b bright_green]Log",
                border_style="bright_green",
                box=box.MINIMAL_DOUBLE_HEAD,
                padding=(0, 1),
            )
        )

def setup_logging(table, layout):
    """Set up logging to both a file and a Rich UI."""
    logger = logging.getLogger("SIGMA DOWNLOADER")
    logger.handlers.clear()
    logger.setLevel(logging.DEBUG)
    file_handler = logging.FileHandler("log.txt", mode="a", encoding="utf-8")
    file_handler.setFormatter(logging.Formatter(
        "%(asctime)s - %(levelname)s - %(message)s"
    ))
    ui_handler = UILogger(table, layout)
    ui_handler.setFormatter(logging.Formatter("%(message)s"))
    logger.addHandler(file_handler)
    logger.addHandler(ui_handler)
    return logger