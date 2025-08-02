# -*- coding: utf-8 -*-
import pyperclip
from rich.live import Live
from time import sleep
from ui.layout import make_layout
from ui.header import Header
from utils.url_utils import detect_url_type
from utils.ffmpeg_utils import check_ffmpeg
from handlers.instagram_handler import download_instagram_media
from handlers.youtube_handler import download_video_audio
from constants import console

def main():
    """Main entry point for the application."""
    check_ffmpeg()
    
    try:
        clipboard_url = pyperclip.paste().strip()
        url_type = detect_url_type(clipboard_url)
        
        if url_type == "unknown":
            raise ValueError("Clipboard does not contain a supported URL.")
        video_url = clipboard_url
        
    except Exception as e:
        console.print(f"[bright_red]Clipboard read failed or unsupported URL:[/] {e}")
        video_url = get_url_from_user()

    layout = make_layout()
    layout["header"].update(Header())

    with Live(layout, refresh_per_second=24, screen=True):
        if url_type == "youtube":
            download_video_audio(video_url, layout)
        else:
            download_instagram_media(video_url, layout)
        sleep(2)

def get_url_from_user() -> str:
    """Prompt user to enter URL manually."""
    while True:
        console.print("[bright_yellow]Enter URL manually (YouTube or Instagram URL. Type 'quit' to exit)[/]")
        video_url = console.input("[cyan]>> [/]").strip()
        
        if video_url.lower() in ("quit", "q", "exit", "e"):
            console.print("[bright_yellow]Exiting...[/]")
            exit(0)
            
        url_type = detect_url_type(video_url)
        if url_type != "unknown":
            return video_url
            
        console.print("[bright_red]Unsupported URL type. Please enter a valid YouTube or Instagram URL.")

if __name__ == "__main__":
    main()