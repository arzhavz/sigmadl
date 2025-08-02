# -*- coding: utf-8 -*-
import os
import re
import requests
from rich.table import Table
from rich.panel import Panel
from rich.columns import Columns
from rich import box
from scrapers.instagram import InstaDL
from utils.url_utils import is_instagram_reel
from utils.file_utils import create_download_folder, format_file_size
from ui.logger import setup_logging
from ui.progress import create_progress

def download_instagram_media(url: str, layout) -> None:
    """Handle Instagram media download process."""
    body_log = Table.grid(padding=1)
    body_log.add_column("Time", style="bright_black", no_wrap=True)
    body_log.add_column("Level", style="bright_green", no_wrap=True)
    body_log.add_column("Message", style="bright_white")
    logger = setup_logging(body_log, layout)
    progress = create_progress()

    layout["body"].update(
        Panel(body_log, title="[b bright_green]Log", border_style="bright_green", 
              box=box.MINIMAL_DOUBLE_HEAD, padding=(0, 1))
    )
    layout["footer"].update(
        Panel(progress, title="[b bright_green]Progress", 
              border_style="bright_green", box=box.SQUARE, padding=(0, 1))
    )

    try:
        scraper = InstaDL()
        logger.info(f"Detected Instagram URL: {url}")
        
        if is_instagram_reel(url):
            result = scraper.Reel(url)
            media_type = "reel"
            ext = "mp4"
        else:
            result = scraper.Photo(url)
            media_type = "photo"
            ext = "jpg"

        if not result["status"] or not result["url"]:
            raise Exception("Failed to get download URL from Instagram")

        media_urls = result["url"]
        logger.info(f"Found {len(media_urls)} media file(s) to download.")

        folder_name = create_download_folder("instagram")
        logger.info(f"Folder created: {folder_name}")

        file_paths = []
        for idx, download_url in enumerate(media_urls, 1):
            file_ext = ext
            if media_type == "photo":
                match = re.search(r'\.(jpg|jpeg|png|webp|gif)(?:\?|$)', download_url, re.IGNORECASE)
                if match:
                    file_ext = match.group(1)
            
            file_path = os.path.join(folder_name, f"{media_type}_{idx}.{file_ext}")
            download_file(download_url, file_path, progress, logger)
            file_paths.append(file_path)

        display_downloaded_files(folder_name, layout)

    except Exception as e:
        logger.error(f"Error: {e}")

def download_file(url: str, file_path: str, progress, logger) -> None:
    """Download a single file with progress tracking."""
    with requests.get(url, stream=True) as r:
        r.raise_for_status()
        total_size = int(r.headers.get('content-length', 0))
        task = progress.add_task(f"Downloading {os.path.basename(file_path)}", total=total_size)
        
        with open(file_path, 'wb') as f:
            for chunk in r.iter_content(chunk_size=8192):
                if chunk:
                    f.write(chunk)
                    progress.update(task, advance=len(chunk))
        
        logger.info(f"File saved as {file_path}")

def display_downloaded_files(folder_name: str, layout) -> None:
    """Display downloaded files in a table format."""
    files = os.listdir(folder_name)
    chunk_size = 6
    tables = []
    
    for i in range(0, len(files), chunk_size):
        chunk = files[i:i+chunk_size]
        file_table = Table(title="[b bright_green]Downloaded Files", box=box.SQUARE)
        file_table.add_column("File Name", style="bright_green")
        file_table.add_column("Size", style="bright_white", justify="right")
        
        for f in chunk:
            file_path = os.path.join(folder_name, f)
            size_bytes = os.path.getsize(file_path)
            file_table.add_row(f, format_file_size(size_bytes))
        
        tables.append(file_table)
    
    layout["footer"].update(
        Panel(
            Columns(tables, expand=True, equal=True),
            border_style="bright_green",
            box=box.SQUARE,
            padding=(0, 1)
        )
    )