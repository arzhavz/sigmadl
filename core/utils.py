# -*- coding: utf-8 -*-
import re

from rich.console import Console

from .constants import (
    FFMPEG_PATH, 
    console
)


def check_ffmpeg():
    if not FFMPEG_PATH:
        console.print("[red bold]ERROR:[/] ffmpeg is not found in PATH. Make sure ffmpeg is installed and PATH is configured.")
        exit(1)

def is_youtube_url(url: str) -> bool:
    pattern = (
        r"^(https?://)?(www\.)?"
        r"(youtube\.com/(watch\?v=|embed/|shorts/|live/)|youtu\.be/)"
        r"[\w\-]{11}([&?][\w=&-]*)?$"
    )
    return re.match(pattern, url) is not None

def is_instagram_reel(url: str) -> bool:
    pattern = r"^https?://(www\.)?instagram\.com/(?:[\w\.\-]+/)?reel/[\w\-]+/?(?:\?.*)?$"
    return re.match(pattern, url) is not None

def is_instagram_photo(url: str) -> bool:
    pattern = r"^https?://(www\.)?instagram\.com/(?:[\w\.\-]+/)?p/[\w\-]+/?(?:\?.*)?$"
    return re.match(pattern, url) is not None

def is_tiktok_url(url: str) -> bool:
    pattern = r"^https?://(www\.)?tiktok\.com/(@[\w\.-]+/video/|v/)?\d+"
    return re.match(pattern, url) is not None

def is_facebook_url(url: str) -> bool:
    pattern = (
        r"^https?://(www\.)?facebook\.com/.+/videos/\d+"
        r"|^https?://(www\.)?facebook\.com/reel/\d+"
    )
    return re.match(pattern, url) is not None

def is_twitter_url(url: str) -> bool:
    pattern = r"^https?://(www\.)?(twitter\.com|x\.com)/.+/status/\d+"
    return re.match(pattern, url) is not None

def detect_url_type(url: str) -> str:
    if is_youtube_url(url):
        return "youtube"
    elif is_instagram_reel(url):
        return "instagram_reel"
    elif is_instagram_photo(url):
        return "instagram_photo"
    elif is_tiktok_url(url):
        return "tiktok"
    elif is_facebook_url(url):
        return "facebook"
    elif is_twitter_url(url):
        return "twitter"
    else:
        return "unknown"

def human_readable_size(size_bytes: int) -> str:
    if size_bytes < 1024:
        return f"{size_bytes} B"
    elif size_bytes < 1024 * 1024:
        return f"{size_bytes / 1024:.1f} KB"
    else:
        return f"{size_bytes / (1024 * 1024):.2f} MB"