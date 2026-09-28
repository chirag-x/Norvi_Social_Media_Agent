import os
import asyncio
from pathlib import Path
import imageio_ffmpeg
from src.utils.logger import logger
import re

class VideoRenderer:
    """
    Handles physical video cutting and rendering using FFmpeg.
    """
    def __init__(self):
        self.output_dir = Path("outputs")
        self.output_dir.mkdir(exist_ok=True)
        self.ffmpeg_path = imageio_ffmpeg.get_ffmpeg_exe()

    def _sanitize_filename(self, name: str) -> str:
        return re.sub(r'[\\/*?:"<>|]', "", name).strip()
        


    async def extract_clip(self, source_video: str, start_time: float, end_time: float, title: str, crop_vertical: bool = True, transcript: list = None) -> str:
        """
        Uses FFmpeg to cut a specific segment of a video and optionally crops to 9:16.
        """
        if not os.path.exists(source_video):
            raise FileNotFoundError(f"Source video not found: {source_video}")
            
        safe_title = self._sanitize_filename(title)
        output_file = self.output_dir / f"{safe_title}.mp4"
        
        duration = end_time - start_time
        
        cmd = [
            self.ffmpeg_path,
            "-y",
            "-ss", str(start_time),
            "-i", source_video,
            "-t", str(duration)
        ]
        
        # Build video filters
        if crop_vertical:
            cmd.extend([
                "-vf", "crop=ih*(9/16):ih",
                "-c:v", "libx264",
                "-preset", "veryfast",
                "-crf", "23",
                "-c:a", "aac",
                "-b:a", "128k"
            ])
        else:
            # Instant stream copy if no filters are applied
            cmd.extend([
                "-c:v", "copy",
                "-c:a", "copy"
            ])
            
        cmd.append(str(output_file))
        
        logger.info(f"Rendering clip: {safe_title.encode('ascii', 'ignore').decode()} [{start_time}s - {end_time}s]")
        
        process = await asyncio.create_subprocess_exec(
            *cmd,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE
        )
        
        try:
            stdout, stderr = await asyncio.wait_for(process.communicate(), timeout=60)
        except asyncio.TimeoutError:
            process.kill()
            raise RuntimeError("FFmpeg rendering timed out.")
            
        if process.returncode != 0:
            err = stderr.decode('utf-8', errors='ignore')
            raise RuntimeError(f"FFmpeg rendering failed: {err}")
            
        logger.info(f"Render successful: {str(output_file).encode('ascii', 'ignore').decode()}")
        return str(output_file.absolute())
