# -*- coding: utf-8 -*-
import re

def is_youtube_url(url: str) -> bool:
    """Check if the given URL is a valid YouTube URL."""
    pattern = (
        r"^(https?://)?(www\.)?"
        r"(youtube\.com/(watch\?v=|embed/|shorts/|live/)|youtu\.be/)"
        r"[\w\-]{11}([&?][\w=&-]*)?$"
    )
    return re.match(pattern, url) is not None

def is_instagram_reel(url: str) -> bool:
    """Check if the given URL is a valid Instagram Reel URL."""
    pattern = r"^https?://(www\.)?instagram\.com/(?:[\w\.\-]+/)?reel/[\w\-]+/?(?:\?.*)?$"
    return re.match(pattern, url) is not None

def is_instagram_photo(url: str) -> bool:
    """Check if the given URL is a valid Instagram Photo URL."""
    pattern = r"^https?://(www\.)?instagram\.com/(?:[\w\.\-]+/)?p/[\w\-]+/?(?:\?.*)?$"
    return re.match(pattern, url) is not None

def detect_url_type(url: str) -> str:
    """Detect the type of URL and return a string indicating the type."""
    if is_youtube_url(url):
        return "youtube"
    elif is_instagram_reel(url):
        return "instagram_reel"
    elif is_instagram_photo(url):
        return "instagram_photo"
    else:
        return "unknown"