import httpx
import json
from typing import List, Dict, AsyncGenerator
from src.config.config import get_config
from src.utils.logger import logger

class ModelManager:
    """
    Manages checking, verifying, and pulling Ollama models.
    """
    _instance = None

    @classmethod
    def get_instance(cls):
        if cls._instance is None:
            cls._instance = ModelManager()
        return cls._instance

    def __init__(self):
        self.config = get_config()
        self.host = self.config.ollama_host
        self.target_model = self.config.ollama_model

    async def list_local_models(self) -> List[str]:
        """Returns a list of model names currently installed in Ollama."""
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(f"{self.host}/api/tags", timeout=5.0)
                if response.status_code == 200:
                    data = response.json()
                    models = [m.get("name") for m in data.get("models", [])]
                    return models
                return []
        except Exception as e:
            logger.error(f"Failed to list local models: {e}")
            return []

    async def has_required_model(self) -> bool:
        """Checks if the required target model is installed or accessible."""
        models = await self.list_local_models()
        
        # Check for exact match, or match without tag if the local model has ':latest'
        if self.target_model in models:
            return True
            
        if ":" not in self.target_model and f"{self.target_model}:latest" in models:
            return True
            
        # If it's not in the local tags, it might be a cloud-backed or alias model.
        # Let's run a quick smoke test. If the API responds successfully, it's accessible.
        logger.info(f"Model {self.target_model} not found in local tags. Attempting smoke test...")
        is_accessible = await self.smoke_test()
        if is_accessible:
            logger.info(f"Smoke test passed! Cloud/alias model {self.target_model} is accessible.")
            return True
            
        return False

    async def pull_model_stream(self) -> AsyncGenerator[Dict, None]:
        """
        Pulls the target model from the Ollama registry, yielding status dicts.
        Dict format: {"status": "downloading...", "completed": 1234, "total": 5678}
        """
        url = f"{self.host}/api/pull"
        payload = {"name": self.target_model}
        
        logger.info(f"Starting pull for model: {self.target_model}")
        
        try:
            async with httpx.AsyncClient() as client:
                async with client.stream("POST", url, json=payload, timeout=None) as response:
                    if response.status_code != 200:
                        yield {"error": f"Failed to pull model (HTTP {response.status_code})"}
                        return
                        
                    async for line in response.aiter_lines():
                        if line:
                            try:
                                data = json.loads(line)
                                yield data
                            except json.JSONDecodeError:
                                pass
        except Exception as e:
            logger.error(f"Stream error pulling model: {e}")
            yield {"error": str(e)}

    async def smoke_test(self) -> bool:
        """
        Runs a minimal prompt against the model to verify it's working.
        """
        url = f"{self.host}/api/generate"
        payload = {
            "model": self.target_model,
            "prompt": "Say 'OK' if you are online.",
            "stream": False,
            "options": {"num_predict": 10}
        }
        
        try:
            async with httpx.AsyncClient() as client:
                response = await client.post(url, json=payload, timeout=15.0)
                return response.status_code == 200
        except Exception as e:
            logger.error(f"Smoke test failed: {e}")
            return False
