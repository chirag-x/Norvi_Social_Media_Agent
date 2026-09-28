import json
import httpx
from typing import List, Dict
from src.utils.logger import logger
from src.app.state import AppState

class GemmaEngine:
    """
    Communicates with local Ollama to analyze transcripts and generate viral clips.
    """
    _instance = None
    
    @classmethod
    def get_instance(cls):
        if cls._instance is None:
            cls._instance = GemmaEngine()
        return cls._instance

    def __init__(self, host="http://127.0.0.1:11434"):
        self.host = host
        self.model = "gemma4:cloud" # Fixed alias requested by user

    async def analyze_transcript(self, transcript: List[Dict], video_context: dict) -> List[Dict]:
        """
        Sends the transcript to Gemma and requests a JSON array of clip candidates.
        """
        # Format the transcript into a readable script for the AI
        script = ""
        for seg in transcript:
            script += f"[{seg['start']:.1f}s - {seg['end']:.1f}s] {seg['text']}\n"
            
        system_prompt = (
            "You are an elite viral social media producer. Your job is to read the timestamped transcript "
            "of a video and identify the absolute best, most engaging, highest-retention moments to extract "
            "into short-form clips (TikTok/Shorts/Reels).\n"
            "You must respond ONLY with a strict JSON array of objects. Do not include markdown code blocks or conversational text.\n"
            "Each object must have these exact keys:\n"
            "- 'title': A catchy, clickbait title for the clip. If a story is too long (over 60s), split it into multiple clips and append '(Part 1)', '(Part 2)' to their titles.\n"
            "- 'start_time': The exact start timestamp in seconds (float).\n"
            "- 'end_time': The exact end timestamp in seconds (float).\n"
            "- 'reasoning': Why this clip is highly engaging.\n"
            "- 'virality_score': A score from 1 to 10.\n"
            "\n"
            "CRITICAL RULES:\n"
            "1. If a highly engaging story is longer than 60-90 seconds, YOU MUST split it into sequential clips (Part 1, Part 2, etc.) so they can be posted as a series.\n"
            "2. Ensure the cut-off point between Part 1 and Part 2 creates a 'cliffhanger' effect to maximize viewer retention for the next part.\n"
        )
        
        user_prompt = (
            f"Video Title: {video_context.get('title', 'Unknown')}\n"
            f"Niche: {video_context.get('niche', 'General')}\n\n"
            f"Transcript:\n{script}\n\n"
            "Analyze this transcript and extract the top 3 best clips as a JSON array."
        )

        logger.info("Sending transcript to Gemma for analysis...")
        
        payload = {
            "model": self.model,
            "prompt": f"{system_prompt}\n\n{user_prompt}",
            "stream": False,
            "format": "json" # Forces Ollama to return JSON
        }
        
        async with httpx.AsyncClient(timeout=120.0) as client:
            try:
                response = await client.post(f"{self.host}/api/generate", json=payload)
                response.raise_for_status()
                data = response.json()
                
                # Parse the returned JSON array
                raw_response = data.get("response", "[]")
                clips = json.loads(raw_response)
                
                if not isinstance(clips, list):
                    logger.warning("Gemma did not return a list. Wrapping in list.")
                    clips = [clips]
                    
                logger.info(f"Gemma successfully extracted {len(clips)} clip(s).")
                return clips
                
            except Exception as e:
                logger.error(f"Gemma Analysis Failed: {e}")
                return []
                
    async def generate_text(self, prompt: str) -> str:
        """
        Sends a generic text prompt to Gemma and returns the raw string response.
        """
        payload = {
            "model": self.model,
            "prompt": prompt,
            "stream": False
        }
        
        async with httpx.AsyncClient(timeout=120.0) as client:
            try:
                response = await client.post(f"{self.host}/api/generate", json=payload)
                response.raise_for_status()
                data = response.json()
                return data.get("response", "").strip()
            except Exception as e:
                logger.error(f"Gemma Text Generation Failed: {e}")
                return f"Error: Could not reach local AI model. {e}"
