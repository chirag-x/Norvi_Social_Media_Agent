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

    async def analyze_transcript(self, transcript: List[Dict], video_context: dict, max_clip_duration: int = 60) -> List[Dict]:
        """
        Sends the transcript to Gemma and requests a JSON array of clip candidates.
        max_clip_duration: hard ceiling in seconds. The AI is instructed to respect it,
        and any clip the AI returns that exceeds it is automatically split in post-processing.
        """
        # Format the transcript into a readable script for the AI
        script = ""
        total_duration = 0.0
        for seg in transcript:
            script += f"[{seg['start']:.1f}s - {seg['end']:.1f}s] {seg['text']}\n"
            total_duration = max(total_duration, seg['end'])
        
        system_prompt = (
            "You are an elite viral social media producer. Your job is to read the timestamped transcript "
            "of a video and identify the absolute best, most engaging, highest-retention moments to extract "
            "into short-form clips (TikTok/Shorts/Reels).\n"
            "You must respond ONLY with a strict JSON array of objects. Do not include markdown code blocks or conversational text.\n"
            "Each object must have these exact keys:\n"
            "- 'title': A catchy, clickbait title for the clip.\n"
            "- 'start_time': The exact start timestamp in seconds (float).\n"
            "- 'end_time': The exact end timestamp in seconds (float).\n"
            "- 'reasoning': Why this clip is highly engaging.\n"
            "- 'virality_score': A score from 1 to 10.\n"
            "\n"
            f"CRITICAL DURATION RULE — THIS IS THE MOST IMPORTANT RULE:\n"
            f"The user has set a MAXIMUM clip duration of {max_clip_duration} seconds.\n"
            f"Every single clip you return MUST have (end_time - start_time) <= {max_clip_duration}.\n"
            f"NO EXCEPTIONS. If a great moment is longer than {max_clip_duration}s, you MUST split it into "
            f"sequential '(Part 1)', '(Part 2)' clips, each under {max_clip_duration} seconds.\n"
            f"NEVER return a clip where end_time - start_time > {max_clip_duration}.\n"
            "\n"
            f"COMPLETENESS RULE:\n"
            f"The video is {total_duration:.1f} seconds long. You MUST scan the ENTIRE video from 0s to {total_duration:.1f}s "
            f"and extract ALL highly engaging segments in ONE response. Do not stop early. "
            f"Do not save clips for a second pass. Return every good clip in this single JSON array.\n"
        )
        
        user_prompt = (
            f"Video Title: {video_context.get('title', 'Unknown')}\n"
            f"Niche: {video_context.get('niche', 'General')}\n"
            f"Total Video Duration: {total_duration:.1f} seconds\n"
            f"Maximum clip duration allowed: {max_clip_duration} seconds\n\n"
            f"Transcript:\n{script}\n\n"
            f"Analyze the ENTIRE transcript from start to finish and extract ALL viral moments as a single JSON array. "
            f"Every clip must be under {max_clip_duration} seconds. Split longer segments into numbered parts."
        )

        logger.info(f"Sending transcript to Gemma (max_duration={max_clip_duration}s, video={total_duration:.1f}s)...")
        
        payload = {
            "model": self.model,
            "prompt": f"{system_prompt}\n\n{user_prompt}",
            "stream": False,
            "format": "json"
        }
        
        # Timeout tuned for very long content (e.g. 3-hour movies):
        # - 30s to establish the connection to Ollama
        # - up to 3600s (1 hour) for the model to finish generating
        timeout = httpx.Timeout(connect=30.0, read=3600.0, write=30.0, pool=30.0)
        async with httpx.AsyncClient(timeout=timeout) as client:
            try:
                response = await client.post(f"{self.host}/api/generate", json=payload)
                response.raise_for_status()
                data = response.json()
                
                raw_response = data.get("response", "[]")
                clips = json.loads(raw_response)
                
                if not isinstance(clips, list):
                    logger.warning("Gemma did not return a list. Wrapping in list.")
                    clips = [clips]
                
                # ── Hard post-processing clamp ─────────────────────────────────
                # If the AI still returned clips over the limit, split them here.
                enforced = []
                for clip in clips:
                    start = float(clip.get('start_time', 0.0))
                    end   = float(clip.get('end_time', 0.0))
                    duration = end - start
                    
                    if duration <= max_clip_duration:
                        enforced.append(clip)
                    else:
                        # Split into equal-sized parts under the limit
                        logger.info(f"Splitting oversized clip '{clip.get('title')}' ({duration:.1f}s) into parts.")
                        import math
                        num_parts = math.ceil(duration / max_clip_duration)
                        part_size = duration / num_parts
                        base_title = clip.get('title', 'Clip')
                        # Strip any existing (Part N) suffix
                        import re
                        base_title = re.sub(r'\s*\(Part \d+\)$', '', base_title, flags=re.IGNORECASE).strip()
                        for i in range(num_parts):
                            p_start = start + i * part_size
                            p_end   = min(start + (i + 1) * part_size, end)
                            part = dict(clip)
                            part['title']      = f"{base_title} (Part {i+1})"
                            part['start_time'] = round(p_start, 1)
                            part['end_time']   = round(p_end, 1)
                            enforced.append(part)
                
                logger.info(f"Gemma extracted {len(clips)} clip(s); after duration enforcement: {len(enforced)} clip(s).")
                return enforced
                
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
        
        async with httpx.AsyncClient(timeout=httpx.Timeout(connect=30.0, read=600.0, write=30.0, pool=30.0)) as client:
            try:
                response = await client.post(f"{self.host}/api/generate", json=payload)
                response.raise_for_status()
                data = response.json()
                return data.get("response", "").strip()
            except Exception as e:
                logger.error(f"Gemma Text Generation Failed: {e}")
                return f"Error: Could not reach local AI model. {e}"
