# -*- coding: utf-8 -*-
import os
import logging
import re
import requests 

from datetime import datetime

from rich import box
from rich.panel import Panel
from rich.layout import Layout
from rich.columns import Columns

from ui.progress import create_progress
from ui.file_table import create_file_table
from core.utils import is_instagram_reel
from scraper.instagram_scraper import InstagramScraper


class InstagramDownloader:
    def __init__(self, layout: Layout, logger: logging.Logger):
        self.layout = layout
        self.logger = logger
        self.progress = create_progress()
        self.scraper = InstagramScraper()

    def download(self, url: str):
        self.layout["footer"].update(
            Panel(self.progress, title="[b bright_green]Progress", border_style="bright_green", box=box.SQUARE, padding=(0, 1))
        )
        try:
            self.logger.info(f"Detected Instagram URL: {url}")
            if is_instagram_reel(url):
                result = self.scraper.get_reel(url)
                media_type = "reel"
                ext = "mp4"
            else:
                result = self.scraper.get_photo(url)
                media_type = "photo"
                ext = "jpg"

            if not result["status"] or not result["url"]:
                raise Exception("Failed to get download URL from Instagram")

            media_urls = result["url"]
            self.logger.info(f"Found {len(media_urls)} media file(s) to download.")

            folder_name = f"instagram_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
            os.makedirs(folder_name, exist_ok=True)
            self.logger.info(f"Folder created: {folder_name}")

            file_paths = []
            for idx, download_url in enumerate(media_urls, 1):
                file_ext = ext
                if media_type == "photo":
                    match = re.search(r'\.(jpg|jpeg|png|webp|gif)(?:\?|$)', download_url, re.IGNORECASE)
                    if match:
                        file_ext = match.group(1)
                file_path = os.path.join(folder_name, f"{media_type}_{idx}.{file_ext}")

                with requests.get(download_url, stream=True) as r:
                    r.raise_for_status()
                    total_size = int(r.headers.get('content-length', 0))
                    task_download = self.progress.add_task(f"Downloading {os.path.basename(file_path)}", total=total_size)
                    downloaded = 0
                    with open(file_path, 'wb') as f:
                        for chunk in r.iter_content(chunk_size=8192):
                            if chunk:
                                f.write(chunk)
                                downloaded += len(chunk)
                                self.progress.update(task_download, completed=downloaded)
                    self.progress.update(task_download, completed=total_size)
                self.logger.info(f"{media_type.capitalize()} saved as {file_path}")
                file_paths.append(file_path)

            files = os.listdir(folder_name)
            chunk_size = 6
            tables = []
            for i in range(0, len(files), chunk_size):
                chunk = files[i:i+chunk_size]
                tables.append(create_file_table(chunk, folder_name))
            self.layout["footer"].update(
                Panel(
                    Columns(tables, expand=True, equal=True),
                    border_style="bright_green",
                    box=box.SQUARE,
                    padding=(0, 1)
                )
            )
        except Exception as e:
            self.logger.error(f"Error: {e}")