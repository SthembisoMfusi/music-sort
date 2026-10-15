import asyncio
from typing import Dict, Any, Optional
import yt_dlp
from ytmusicapi import YTMusic

class MediaExtractorService:
    def __init__(self):
        self.ytm = YTMusic()

    async def search_music(self, query: str, filter_type: str = "songs") -> list:
        """
        Searches YouTube music for tracks, videos, or albums.
        Runs inside a thread pool to keep the main async loop free.

        Args:
            query (str): The search query
            filter_type (str): Type of content to search for (songs, videos, albums)

        Returns:
            list: List of search results
        """
        loop = asyncio.get_event_loop()
        results = await loop.run_in_executor(
            None, lambda: self.ytm.search(query, filter=filter_type)
        )
        parsed_results = []
        for item in results:
            parsed_results.append({
                "id": item.get("videoId", ""),
                "title": item.get("title", ""),
                "artists": item.get("artists", []),
                "album": item.get("album", {}),
                "duration": item.get("duration", ""),
                "thumbnails": item.get("thumbnails", []),
                "type": item.get("resultType", "")
            })
        return  parsed_results
    async def get_stream_url(self, video_id: str, mode: str = "audio")-> Optional[str]:
        """
        Extracts the stream URL for a given video ID.

        Args:
            video_id (str): The YouTube video ID
            mode (str): The mode of extraction (audio or video)

        Returns:
            str: The stream URL
        """
        loop = asyncio.get_event_loop()
        url = f"https://www.youtube.com/{video_id}"
        ydl_opts = {
            'format': 'bestaudio/best' if mode == 'audio' else 'best',
            'noplaylist': True,
            'nocheckcertificate': True,
            'ignoreerrors': False,
            'logtostderr': False,
            'quiet': True,
            'no_warnings': True,
            'default_search': 'error',
            'source_address': '0.0.0.0',
            'prefer_ffmpeg': True,
            'skip_download': True
        }

        if mode == 'audio':
            ydl_opts['format'] = 'bestaudio/best'
        else:
            ydl_opts['format'] = 'best[ext=mp4]'

        try:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = await loop.run_in_executor(None, lambda: ydl.extract_info(url, download=False))
                if info and "url" in info:
                    return info["url"]
        except Exception as e:
            print(f"Error extracting stream URL: {e}")
            return None
