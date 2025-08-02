# -*- coding: utf-8 -*-
import yt_dlp
from typing import Dict

def get_video_info(url: str) -> Dict:
    """Get YouTube video information using yt-dlp."""
    with yt_dlp.YoutubeDL({'quiet': True}) as ydl:
        return ydl.extract_info(url, download=False)