import asyncio
from typing import List, Dict
from faster_whisper import WhisperModel
from src.utils.logger import logger

class WhisperTranscriber:
    """
    Handles local audio transcription using faster-whisper.
    """
    _instance = None
    
    @classmethod
    def get_instance(cls):
        if cls._instance is None:
            cls._instance = WhisperTranscriber()
        return cls._instance

    def __init__(self, model_size="base"):
        self.model_size = model_size
        self.model = None

    def _load_model(self):
        if self.model is None:
            logger.info(f"Loading Whisper model ({self.model_size})...")
            # Uses CPU by default for maximum compatibility. 
            # Can be switched to 'cuda' for NVIDIA GPUs.
            self.model = WhisperModel(self.model_size, device="cpu", compute_type="int8")

    async def transcribe(self, audio_path: str, progress_callback=None) -> List[Dict]:
        """
        Transcribes an audio file into timestamped segments.
        Returns a list of dicts: {"start": float, "end": float, "text": str}
        """
        logger.info(f"Starting transcription for {audio_path}")
        return await asyncio.to_thread(self._sync_transcribe, audio_path, progress_callback)

    def _sync_transcribe(self, audio_path: str, progress_callback=None) -> List[Dict]:
        if self.model is None and progress_callback:
            progress_callback("Initializing AI Model (May download on first run)...")
            
        self._load_model()
        
        if progress_callback:
            progress_callback("Analyzing audio...")
            
        segments, info = self.model.transcribe(audio_path, beam_size=5)
        
        logger.info(f"Detected language: {info.language} with probability {info.language_probability}")
        
        results = []
        for segment in segments:
            res = {
                "start": segment.start,
                "end": segment.end,
                "text": segment.text.strip()
            }
            results.append(res)
            # In a long video, updating for every segment gives a nice live feel
            if progress_callback:
                progress_callback(f"Transcribing: [{segment.start:.1f}s] {res['text']}")
                
        return results
