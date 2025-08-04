# -*- coding: utf-8 -*-
import os
import yt_dlp
import logging

from rich import box
from rich.panel import Panel
from rich.layout import Layout

from ui.progress import create_progress
from ui.file_table import create_file_table
from core.constants import FFMPEG_PATH


class YouTubeDownloader:
    def __init__(self, layout: Layout, logger: logging.Logger):
        self.layout = layout
        self.logger = logger
        self.progress = create_progress()

    def download(self, video_url: str):
        self.layout["footer"].update(
            Panel(self.progress, title="[b bright_green]Progress", border_style="bright_green", box=box.SQUARE, padding=(0, 1))
        )
        try:
            self.logger.info(f"Detected YouTube URL: {video_url}")
            with yt_dlp.YoutubeDL({'quiet': True}) as ydl:
                info = ydl.extract_info(video_url, download=False)
                title = info.get('title', 'video')
                safe_title = yt_dlp.utils.sanitize_filename(title)

            folder_name = safe_title
            os.makedirs(folder_name, exist_ok=True)
            self.logger.info(f"Title: {title}")
            self.logger.info(f"Folder created: {folder_name}")

            def video_hook(d):
                if d['status'] == 'downloading':
                    total = d.get("total_bytes") or d.get("total_bytes_estimate") or 100
                    downloaded = d.get("downloaded_bytes", 0)
                    self.progress.update(task_video, completed=downloaded, total=total)
                elif d['status'] == 'finished':
                    self.progress.update(task_video, completed=self.progress.tasks[task_video].total)

            merged_opts = {
                'format': 'bestvideo[height<=1080]+bestaudio/bestvideo+bestaudio/best',
                'outtmpl': f'{folder_name}/{safe_title}_video.%(ext)s',
                'merge_output_format': 'mp4',
                'quiet': True,
                'no_warnings': True,
                'ffmpeg_location': FFMPEG_PATH,
                'progress_hooks': [video_hook],
            }
            task_video = self.progress.add_task("Downloading video", total=100)
            with yt_dlp.YoutubeDL(merged_opts) as ydl:
                ydl.download([video_url])
            self.progress.update(task_video, completed=self.progress.tasks[task_video].total)
            self.logger.info("Video saved as MP4")

            def audio_hook(d):
                if d['status'] == 'downloading':
                    total = d.get("total_bytes") or d.get("total_bytes_estimate") or 100
                    downloaded = d.get("downloaded_bytes", 0)
                    self.progress.update(task_audio, completed=downloaded, total=total)
                elif d['status'] == 'finished':
                    self.progress.update(task_audio, completed=self.progress.tasks[task_audio].total)

            audio_opts = {
                'format': 'bestaudio[abr<=320]/bestaudio',
                'outtmpl': f'{folder_name}/{safe_title}_audio.%(ext)s',
                'quiet': True,
                'no_warnings': True,
                'ffmpeg_location': FFMPEG_PATH,
                'postprocessors': [{
                    'key': 'FFmpegExtractAudio',
                    'preferredcodec': 'mp3',
                    'preferredquality': '320',
                }],
                'progress_hooks': [audio_hook],
            }
            task_audio = self.progress.add_task("Downloading audio", total=100)
            with yt_dlp.YoutubeDL(audio_opts) as ydl:
                ydl.download([video_url])
            self.progress.update(task_audio, completed=self.progress.tasks[task_audio].total)
            self.logger.info("Audio saved as MP3")

            files = os.listdir(folder_name)
            file_table = create_file_table(files, folder_name)
            self.layout["footer"].update(
                Panel(file_table, border_style="bright_green", box=box.SQUARE, padding=(0, 1))
            )
        except Exception as e:
            self.logger.error(f"Error: {e}")