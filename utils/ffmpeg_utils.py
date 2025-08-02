# -*- coding: utf-8 -*-
from constants import console, FFMPEG_PATH

def check_ffmpeg():
    """Check if ffmpeg is installed and available in the system PATH."""
    if not FFMPEG_PATH:
        console.print("[red bold]ERROR:[/] ffmpeg is not found in PATH. Make sure ffmpeg is installed and PATH is configured.")
        exit(1)