# -*- coding: utf-8 -*-
import shutil

from rich.console import Console


FFMPEG_PATH = shutil.which("ffmpeg")
VERSION = "1.0.3.1"
LOG_FILE = "log.txt"
console = Console()