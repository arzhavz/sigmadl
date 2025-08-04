# -*- coding: utf-8 -*-
import pyperclip
from time import sleep  
from rich.live import Live

from core import *
from downloader import *
from ui import *


class SigmaDLApp:
    def __init__(self):
        self.layout = make_layout()
        self.layout["header"].update(HeaderPanel(VERSION))
        self.log_table = create_log_table()
        self.logger = setup_logging(self.log_table, self.layout)

    def get_url(self) -> tuple[str, str]:
        try:
            clipboard_url = pyperclip.paste().strip()
            url_type = detect_url_type(clipboard_url)
            if url_type == "unknown":
                raise ValueError("Clipboard does not contain a supported URL.")
            return clipboard_url, url_type
        except Exception as e:
            console.print(f"[bright_red]Clipboard read failed or unsupported URL:[/] {e}")
            while True:
                console.print("[bright_yellow]Enter URL manually (YouTube or Instagram URL. Type 'quit' to exit)[/]")
                video_url = console.input("[cyan]>> [/]").strip()
                if video_url.lower() in ("quit", "q", "exit", "e"):
                    console.print("[bright_yellow]Exiting...[/]")
                    exit(0)
                url_type = detect_url_type(video_url)
                if url_type != "unknown":
                    return video_url, url_type
                console.print("[bright_red]Unsupported URL type. Please enter a valid YouTube or Instagram URL.")

    def run(self):
        check_ffmpeg()
        url, url_type = self.get_url()
        with Live(self.layout, refresh_per_second=24, screen=True):
            if url_type == "youtube":
                downloader = YouTubeDownloader(self.layout, self.logger)
            elif url_type.startswith("instagram"):
                downloader = InstagramDownloader(self.layout, self.logger)
            elif url_type == "tiktok":
                downloader = TikTokDownloader(self.layout, self.logger)
            elif url_type == "facebook":
                downloader = FacebookDownloader(self.layout, self.logger)
            elif url_type == "twitter":
                downloader = TwitterDownloader(self.layout, self.logger)
            else:
                self.logger.error("Unsupported URL type.")
                return
            downloader.download(url)
            sleep(2)

def main():
    SigmaDLApp().run()

if __name__ == "__main__":
    main()
