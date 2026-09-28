import os
import shutil
import subprocess
import httpx
import asyncio
from typing import Tuple
from src.config.config import get_config
from src.utils.logger import logger

class OllamaManager:
    """
    Manages the local Ollama runtime.
    Ensures Ollama is installed, starts it silently if not running,
    and cleanly stops it on exit (only if this app started it).
    """
    _instance = None

    @classmethod
    def get_instance(cls):
        if cls._instance is None:
            cls._instance = OllamaManager()
        return cls._instance

    def __init__(self):
        self.config = get_config()
        self.host = self.config.ollama_host
        self.process = None
        self.we_started_it = False
        
    def is_installed(self) -> bool:
        """Checks if the ollama executable is in the system PATH."""
        return shutil.which("ollama") is not None

    async def is_running(self) -> bool:
        """Hits the Ollama API to check if it's currently responding."""
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(f"{self.host}/api/tags", timeout=2.0)
                return response.status_code == 200
        except httpx.RequestError:
            return False

    async def start_silently(self) -> Tuple[bool, str]:
        """
        Starts Ollama silently if it isn't already running.
        Returns (success, message).
        """
        if not self.is_installed():
            return False, "Ollama is not installed on this system. Please install it first."
            
        if await self.is_running():
            # If we didn't start it previously, then it's external.
            if not self.we_started_it:
                logger.info("Ollama is already running externally.")
            return True, "Ollama is already running."
            
        logger.info("Starting local Ollama instance...")
        try:
            # CREATE_NO_WINDOW = 0x08000000 on Windows
            creationflags = 0x08000000 if os.name == 'nt' else 0
            
            self.process = subprocess.Popen(
                ["ollama", "serve"],
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
                creationflags=creationflags
            )
            self.we_started_it = True
            
            # Wait for it to spin up
            for _ in range(10):
                await asyncio.sleep(1)
                if await self.is_running():
                    logger.info("Ollama started successfully.")
                    return True, "Started successfully."
                    
            return False, "Ollama process started, but API is not responding."
            
        except Exception as e:
            logger.error(f"Failed to start Ollama: {e}")
            return False, f"Failed to start Ollama: {e}"

    def stop_safely(self):
        """
        Stops the Ollama process only if we started it.
        """
        if self.we_started_it and self.process:
            logger.info("Stopping the Ollama instance we started...")
            try:
                # Terminate gently
                self.process.terminate()
                self.process.wait(timeout=5)
            except subprocess.TimeoutExpired:
                logger.warning("Ollama did not terminate gently, killing...")
                self.process.kill()
            except Exception as e:
                logger.error(f"Error stopping Ollama: {e}")
            finally:
                self.process = None
                self.we_started_it = False
        else:
            logger.info("Leaving Ollama running (we did not start it).")
