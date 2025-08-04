# -*- coding: utf-8 -*-
import os
import yt_dlp
import logging

from datetime import datetime

from rich import box
from rich.panel import Panel
from rich.layout import Layout

from ui.progress import create_progress
from ui.file_table import create_file_table
from core.constants import FFMPEG_PATH


class FacebookDownloader:
    def __init__(self, layout: Layout, logger: logging.Logger):
        self.layout = layout
        self.logger = logger
        self.progress = create_progress()

    def download(self, url: str):
        self.layout["footer"].update(
            Panel(self.progress, title="[b bright_green]Progress", border_style="bright_green", box=box.SQUARE, padding=(0, 1))
        )

        try:
            self.logger.info(f"Detected Facebook video URL: {url}")
            with yt_dlp.YoutubeDL({'quiet': True}) as ydl:
                info = ydl.extract_info(url, download=False)
                title = info.get('title', 'facebook_video')
                safe_title = yt_dlp.utils.sanitize_filename(title)

            folder_name = "facebook_" + datetime.now().strftime("%Y%m%d_%H%M%S")
            os.makedirs(folder_name, exist_ok=True)
            self.logger.info(f"Title: {title}")
            self.logger.info(f"Folder created: {folder_name}")

            def progress_hook(d):
                if d['status'] == 'downloading':
                    total = d.get("total_bytes") or d.get("total_bytes_estimate") or 100
                    downloaded = d.get("downloaded_bytes", 0)
                    self.progress.update(task_id, completed=downloaded, total=total)
                elif d['status'] == 'finished':
                    self.progress.update(task_id, completed=self.progress.tasks[task_id].total)

            ydl_opts = {
                'format': 'bestvideo+bestaudio/best',
                'outtmpl': f'{folder_name}/{safe_title}.%(ext)s',
                'quiet': True,
                'no_warnings': True,
                'progress_hooks': [progress_hook],
                'ffmpeg_location': FFMPEG_PATH,
                'merge_output_format': 'mp4',
            }

            task_id = self.progress.add_task("Downloading Facebook video", total=100)
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                ydl.download([url])
            self.progress.update(task_id, completed=self.progress.tasks[task_id].total)

            self.logger.info("Facebook video downloaded successfully.")

            files = os.listdir(folder_name)
            file_table = create_file_table(files, folder_name)
            self.layout["footer"].update(
                Panel(file_table, border_style="bright_green", box=box.SQUARE, padding=(0, 1))
            )

        except Exception as e:
            self.logger.error(f"Error: {e}")