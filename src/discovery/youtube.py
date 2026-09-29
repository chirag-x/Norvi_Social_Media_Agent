import asyncio
import yt_dlp
from typing import List
from src.discovery.provider import DiscoveryProvider, VideoResult
from src.utils.logger import logger

class YouTubeProvider(DiscoveryProvider):
    """
    Scrapes YouTube search results using yt-dlp.
    """
    async def search(self, query: str, niche: str, duration_filter: str = "Any Length", max_results: int = 100) -> List[VideoResult]:
        logger.info(f"Searching YouTube (via yt-dlp) for: {query} (Niche: {niche}, Duration: {duration_filter})")
        
        try:
            # We fetch more results than needed because we will filter them out
            results = await asyncio.to_thread(self._sync_search, query, max_results)
            
            videos = []
            for res in results:
                try:
                    duration_sec = res.get('duration') or 0
                    
                    # Apply duration filtering
                    if duration_filter == "0 - 3 mins" and (duration_sec == 0 or duration_sec > 180):
                        continue
                    elif duration_filter == "3 - 10 mins" and (duration_sec <= 180 or duration_sec > 600):
                        continue
                    elif duration_filter == "10 - 20 mins" and (duration_sec <= 600 or duration_sec > 1200):
                        continue
                    elif duration_filter == "20+ mins" and duration_sec <= 1200:
                        continue
                    # Extract best thumbnail
                    thumbs = res.get('thumbnails', [])
                    thumb_url = thumbs[-1]['url'] if thumbs else ''
                    
                    video = VideoResult(
                        id=res.get('id', ''),
                        title=res.get('title', 'Unknown Title'),
                        url=res.get('url', ''),
                        channel=res.get('uploader', 'Unknown'),
                        views=res.get('view_count') or 0,
                        publish_date=res.get('upload_date', 'Unknown'),
                        duration=self._format_duration(duration_sec),
                        thumbnail=thumb_url,
                        niche=niche
                    )
                    videos.append(video)
                except Exception as e:
                    logger.warning(f"Failed to parse yt-dlp result: {e}")
                    
            # Sort by highest views first
            videos.sort(key=lambda x: x.views, reverse=True)
            return videos[:5]
            
        except Exception as e:
            logger.error(f"YouTube search failed: {e}")
            return []

    async def get_by_url(self, url: str) -> List[VideoResult]:
        logger.info(f"Direct link detected. Fetching metadata for: {url}")
        try:
            ydl_opts = {'quiet': True, 'extract_flat': True}
            def fetch():
                with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                    return ydl.extract_info(url, download=False)
                    
            res = await asyncio.to_thread(fetch)
            if not res:
                return []
                
            thumbs = res.get('thumbnails', [])
            thumb_url = thumbs[-1]['url'] if thumbs else ''
            
            video = VideoResult(
                id=res.get('id', ''),
                title=res.get('title', 'Unknown Title'),
                url=res.get('webpage_url', res.get('url', url)),
                channel=res.get('uploader', 'Unknown'),
                views=res.get('view_count') or 0,
                publish_date=res.get('upload_date', 'Unknown'),
                duration=self._format_duration(res.get('duration') or 0),
                thumbnail=thumb_url,
                niche="Direct Link"
            )
            return [video]
            
        except Exception as e:
            logger.error(f"Direct URL fetch failed: {e}")
            return []

    def _sync_search(self, query: str, max_results: int):
        ydl_opts = {
            'quiet': True,
            'extract_flat': True,
            'force_generic_extractor': False,
        }
        
        search_query = f"ytsearch{max_results}:{query}"
        
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(search_query, download=False)
            if 'entries' in info:
                return info['entries']
            return []
            
    def _format_duration(self, seconds: int) -> str:
        if not seconds:
            return "0:00"
        m, s = divmod(seconds, 60)
        h, m = divmod(m, 60)
        if h > 0:
            return f"{h}:{m:02d}:{s:02d}"
        return f"{m}:{s:02d}"
