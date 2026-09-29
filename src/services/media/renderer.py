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
        
        from src.storage.database.database import DatabaseManager
        db = DatabaseManager.get_instance()
        
        # Phase 28: Hardware / Thread Limits
        ffmpeg_threads = db.get_setting("ffmpeg_threads", "Auto")
        ffmpeg_hwaccel = db.get_setting("ffmpeg_hwaccel", "None (CPU)")
        
        cmd = [self.ffmpeg_path, "-y"]
        
        # Apply hardware acceleration decoder if selected
        if ffmpeg_hwaccel == "NVIDIA (NVENC)":
            cmd.extend(["-hwaccel", "cuda"])
        elif ffmpeg_hwaccel == "AMD (AMF)":
            cmd.extend(["-hwaccel", "d3d11va"])
        elif ffmpeg_hwaccel == "Intel (QSV)":
            cmd.extend(["-hwaccel", "qsv"])
            
        cmd.extend([
            "-ss", str(start_time),
            "-i", source_video,
            "-t", str(duration)
        ])
        
        # Build video filters
        if crop_vertical:
            encoder = "libx264"
            
            # Apply hardware encoder if selected
            if ffmpeg_hwaccel == "NVIDIA (NVENC)":
                encoder = "h264_nvenc"
            elif ffmpeg_hwaccel == "AMD (AMF)":
                encoder = "h264_amf"
            elif ffmpeg_hwaccel == "Intel (QSV)":
                encoder = "h264_qsv"
                
            cmd.extend([
                "-vf", "crop=ih*(9/16):ih",
                "-c:v", encoder,
                "-preset", "veryfast",
                "-c:a", "aac",
                "-b:a", "128k"
            ])
            # -crf is mainly for libx264, nvenc uses -cq
            if encoder == "libx264":
                cmd.extend(["-crf", "23"])
            elif encoder == "h264_nvenc":
                cmd.extend(["-cq", "23"])
                
            # Apply Thread Limits (only if not Auto)
            if ffmpeg_threads != "Auto":
                cmd.extend(["-threads", str(ffmpeg_threads)])

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
