import asyncio
from typing import List, Dict
import httpx
from src.utils.logger import logger
from PySide6.QtCore import QSettings

class WhisperTranscriber:
    """
    Handles audio transcription using either local faster-whisper or Groq Cloud API.
    """
    _instance = None
    
    @classmethod
    def get_instance(cls):
        if cls._instance is None:
            cls._instance = WhisperTranscriber()
        return cls._instance

    def __init__(self):
        self.local_model_instance = None
        self.current_local_size = None

    async def transcribe(self, audio_path: str, progress_callback=None) -> List[Dict]:
        """
        Transcribes an audio file into timestamped segments.
        Returns a list of dicts: {"start": float, "end": float, "text": str}
        """
        logger.info(f"Starting transcription for {audio_path}")
        
        settings = QSettings("Nexus", "SocialMediaAgent")
        engine = settings.value("transcription_engine", "Local (Faster-Whisper)")
        
        if "Cloud" in engine:
            return await self._transcribe_cloud(audio_path, progress_callback)
        else:
            return await asyncio.to_thread(self._sync_transcribe_local, audio_path, progress_callback)

    async def _transcribe_cloud(self, audio_path: str, progress_callback=None) -> List[Dict]:
        settings = QSettings("Nexus", "SocialMediaAgent")
        api_key = settings.value("groq_api_key", "")
        model_name = settings.value("cloud_whisper_model", "whisper-large-v3-turbo")
        
        if not api_key:
            raise ValueError("Groq API key is missing. Please configure it in Settings.")
            
        if progress_callback:
            progress_callback("Uploading to Groq Cloud API (blazing fast!)...")
            
        url = "https://api.groq.com/openai/v1/audio/transcriptions"
        headers = {
            "Authorization": f"Bearer {api_key}"
        }
        
        # Groq expects a file upload. We use the 'verbose_json' format to get timestamps
        data = {
            "model": model_name,
            "response_format": "verbose_json"
        }
        
        try:
            with open(audio_path, "rb") as f:
                files = {
                    "file": (audio_path, f, "audio/mpeg")
                }
                
                async with httpx.AsyncClient(timeout=120.0) as client:
                    response = await client.post(url, headers=headers, data=data, files=files)
                    response.raise_for_status()
                    result = response.json()
                    
                    segments = result.get("segments", [])
                    results = []
                    for seg in segments:
                        res = {
                            "start": float(seg["start"]),
                            "end": float(seg["end"]),
                            "text": seg["text"].strip()
                        }
                        results.append(res)
                        
                    if progress_callback:
                        progress_callback("Groq transcription complete!")
                        
                    return results
        except httpx.HTTPStatusError as e:
            err_msg = e.response.text
            raise Exception(f"Groq API Error: {err_msg}")
        except Exception as e:
            raise Exception(f"Cloud transcription failed: {str(e)}")

    def _sync_transcribe_local(self, audio_path: str, progress_callback=None) -> List[Dict]:
        from faster_whisper import WhisperModel
        settings = QSettings("Nexus", "SocialMediaAgent")
        model_size = settings.value("local_whisper_model", "base")
        
        # Reload model if size changed
        if self.local_model_instance is None or self.current_local_size != model_size:
            if progress_callback:
                progress_callback(f"Loading local Whisper model ({model_size})...")
            self.local_model_instance = WhisperModel(model_size, device="cpu", compute_type="int8")
            self.current_local_size = model_size
            
        if progress_callback:
            progress_callback("Analyzing audio locally...")
            
        segments, info = self.local_model_instance.transcribe(audio_path, beam_size=5)
        
        logger.info(f"Detected language: {info.language} with probability {info.language_probability}")
        
        results = []
        for segment in segments:
            res = {
                "start": segment.start,
                "end": segment.end,
                "text": segment.text.strip()
            }
            results.append(res)
            if progress_callback:
                progress_callback(f"Transcribing: [{segment.start:.1f}s] {res['text']}")
                
        return results
