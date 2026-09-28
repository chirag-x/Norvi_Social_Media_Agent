import os
import asyncio
import yt_dlp
import re
from pathlib import Path
import imageio_ffmpeg
from src.utils.logger import logger

class MediaProcessor:
    """
    Handles downloading video via yt-dlp and extracting audio via bundled FFmpeg.
    """
    def __init__(self):
        self.cache_dir = Path("cache")
        self.cache_dir.mkdir(exist_ok=True)
        self.ffmpeg_path = imageio_ffmpeg.get_ffmpeg_exe()
        logger.info(f"Using bundled FFmpeg at: {self.ffmpeg_path}")

    def _sanitize_filename(self, name: str) -> str:
        """Removes invalid characters for Windows filenames."""
        return re.sub(r'[\\/*?:"<>|]', "", name).strip()

    async def download_and_prepare(self, url: str, title: str, progress_callback=None) -> dict:
        """
        Downloads best video/audio and extracts an audio-only track.
        Returns paths to both files.
        """
        safe_title = self._sanitize_filename(title)
        video_out = self.cache_dir / f"{safe_title}.mp4"
        audio_out = self.cache_dir / f"{safe_title}.wav"
        
        # If already cached
        if video_out.exists() and audio_out.exists():
            if progress_callback:
                progress_callback(100, "Using cached media.")
            return {"video": str(video_out), "audio": str(audio_out)}

        ydl_opts = {
            'format': 'bestvideo[height<=1080][ext=mp4]+bestaudio[ext=m4a]/best[height<=1080][ext=mp4]/best',
            'merge_output_format': 'mp4',
            'outtmpl': str(video_out),
            'quiet': True,
            'no_warnings': True,
            'ffmpeg_location': self.ffmpeg_path,
            'extractor_args': {
                'youtube': ['player_client=ios,android,web']
            },
            'http_headers': {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
            }
        }

        def hook(d):
            if d['status'] == 'downloading' and progress_callback:
                try:
                    percent_str = d.get('_percent_str', '0%').replace('%', '').strip()
                    percent_str = re.sub(r'\x1b\[[0-9;]*m', '', percent_str)
                    percent = float(percent_str)
                    progress_callback(int(percent * 0.8), "Downloading video...") # 0-80% is download
                except Exception:
                    # Fallback if percent fails to parse
                    progress_callback(40, "Downloading video...")
            elif d['status'] == 'finished' and progress_callback:
                progress_callback(80, "Download finished. Extracting audio...")

        ydl_opts['progress_hooks'] = [hook]

        logger.info(f"Downloading media for {safe_title.encode('ascii', 'ignore').decode()}...")
        
        try:
            # Download video
            await asyncio.to_thread(self._run_yt_dlp, ydl_opts, url)
            
            # Extract Audio using bundled ffmpeg
            if progress_callback:
                progress_callback(85, "Running FFmpeg audio extraction...")
                
            await self._extract_audio(str(video_out), str(audio_out))
            
            if progress_callback:
                progress_callback(100, "Media ready!")
                
            return {"video": str(video_out), "audio": str(audio_out)}
            
        except Exception as e:
            logger.error(f"Media preparation failed: {e}")
            # Cleanup on error
            if video_out.exists():
                video_out.unlink()
            if audio_out.exists():
                audio_out.unlink()
            raise Exception(f"Failed to prepare media: {str(e)}")

    def _run_yt_dlp(self, opts, url):
        with yt_dlp.YoutubeDL(opts) as ydl:
            ydl.download([url])

    async def _extract_audio(self, video_path: str, audio_path: str):
        """Extracts 16kHz mono WAV suitable for transcription."""
        cmd = [
            self.ffmpeg_path,
            "-y", # Overwrite
            "-i", video_path,
            "-vn", # No video
            "-acodec", "pcm_s16le",
            "-ar", "16000",
            "-ac", "1",
            audio_path
        ]
        
        process = await asyncio.create_subprocess_exec(
            *cmd,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE
        )
        try:
            stdout, stderr = await asyncio.wait_for(process.communicate(), timeout=300)
        except asyncio.TimeoutError:
            process.kill()
            raise RuntimeError("FFmpeg extraction timed out after 5 minutes.")
        
        if process.returncode != 0:
            err = stderr.decode('utf-8', errors='ignore')
            raise RuntimeError(f"FFmpeg extraction failed: {err}")
