# -*- coding: utf-8 -*-
import os
from datetime import datetime

def create_download_folder(base_name: str) -> str:
    """Create a timestamped download folder."""
    folder_name = f"{base_name}_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
    os.makedirs(folder_name, exist_ok=True)
    return folder_name

def format_file_size(size_bytes: int) -> str:
    """Format file size in human-readable format."""
    if size_bytes < 1024:
        return f"{size_bytes} B"
    elif size_bytes < 1024 * 1024:
        return f"{size_bytes / 1024:.1f} KB"
    return f"{size_bytes / (1024 * 1024):.2f} MB"