# -*- coding: utf-8 -*-
import os
import yt_dlp
from rich.table import Table
from rich.panel import Panel
from rich import box
from constants import FFMPEG_PATH
from ui.logger import setup_logging
from ui.progress import create_progress
from utils.file_utils import format_file_size
from scrapers.youtube import get_video_info

def download_video_audio(video_url: str, layout) -> None:
    """Handle YouTube video and audio download process."""
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
        logger.info(f"Detected YouTube URL: {video_url}")
        info = get_video_info(video_url)
        title = info.get('title', 'video')
        safe_title = yt_dlp.utils.sanitize_filename(title)
        folder_name = safe_title
        os.makedirs(folder_name, exist_ok=True)
        
        logger.info(f"Title: {title}")
        logger.info(f"Folder created: {folder_name}")

        logger.info("Starting video download...")
        download_video(video_url, folder_name, safe_title, progress, logger)
        logger.info("Video download completed. Now downloading audio...")
        download_audio(video_url, folder_name, safe_title, progress, logger)
        logger.info("Audio download completed.")
        display_downloaded_files(folder_name, layout)

    except Exception as e:
        logger.error(f"Error: {e}")

def download_video(url: str, folder: str, title: str, progress, logger) -> None:
    """Download YouTube video."""
    def video_hook(d):
        if d['status'] == 'downloading':
            total = d.get("total_bytes") or d.get("total_bytes_estimate") or 100
            progress.update(task, completed=d.get("downloaded_bytes", 0), total=total)
        elif d['status'] == 'finished':
            progress.update(task, completed=progress.tasks[task].total)

    opts = {
        'format': 'bestvideo[height<=1080]+bestaudio/bestvideo+bestaudio/best',
        'outtmpl': f'{folder}/{title}_video.%(ext)s',
        'merge_output_format': 'mp4',
        'quiet': True,
        'no_warnings': True,
        'ffmpeg_location': FFMPEG_PATH,
        'progress_hooks': [video_hook],
    }
    
    task = progress.add_task("Downloading video", total=100)
    with yt_dlp.YoutubeDL(opts) as ydl:
        ydl.download([url])
    logger.info("Video saved as MP4")

def download_audio(url: str, folder: str, title: str, progress, logger) -> None:
    """Download YouTube audio."""
    def audio_hook(d):
        if d['status'] == 'downloading':
            total = d.get("total_bytes") or d.get("total_bytes_estimate") or 100
            progress.update(task, completed=d.get("downloaded_bytes", 0), total=total)
        elif d['status'] == 'finished':
            progress.update(task, completed=progress.tasks[task].total)

    opts = {
        'format': 'bestaudio[abr<=320]/bestaudio',
        'outtmpl': f'{folder}/{title}_audio.%(ext)s',
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
    
    task = progress.add_task("Downloading audio", total=100)
    with yt_dlp.YoutubeDL(opts) as ydl:
        ydl.download([url])
    logger.info("Audio saved as MP3")

def display_downloaded_files(folder_name: str, layout) -> None:
    """Display downloaded files in a table."""
    file_table = Table(title="[b bright_green]Downloaded Files", box=box.SQUARE)
    file_table.add_column("File Name", style="bright_green")
    file_table.add_column("Size", style="bright_white", justify="right")
    
    for f in os.listdir(folder_name):
        file_path = os.path.join(folder_name, f)
        size_bytes = os.path.getsize(file_path)
        file_table.add_row(f, format_file_size(size_bytes))
    
    layout["footer"].update(
        Panel(file_table, border_style="bright_green", box=box.SQUARE, padding=(0, 1))
    )