import httpx
from typing import Tuple, Optional
from src.config.config import get_config
from src.services.auth.hwid import get_hardware_id
from src.utils.logger import logger

class AuthClient:
    """
    Handles communication with the Nexus backend for authentication and licensing.
    """
    def __init__(self):
        self.config = get_config()
        self.api_url = self.config.nexus_api_url

    async def login(self, email: str, password: str, activation_key: str) -> Tuple[bool, str, Optional[str]]:
        """
        Attempts to authenticate with the backend.
        Returns: (success, message, token)
        """
        hwid = get_hardware_id()
        
        payload = {
            "email": email,
            "password": password,
            "activation_key": activation_key,
            "hardware_id": hwid
        }
        
        logger.info(f"Attempting login for {email} with HWID {hwid[:8]}...")

        # In a real environment, we send this to the real endpoint.
        # Since the actual backend is out of scope and the API URL is a placeholder,
        # we will simulate a success response if the URL is local/mocked, 
        # or attempt the real request if the user has configured a real URL.
        
        if self.api_url == "https://api.nexus.local":
            # MOCK LOGIN for local development/testing
            logger.info("Using mock authentication because NORVI_API_URL is local.")
            if email and password and activation_key:
                return True, "Login successful", "mock_secure_token_12345"
            else:
                return False, "Please fill in all fields", None
                
        try:
            async with httpx.AsyncClient() as client:
                response = await client.post(f"{self.api_url}/v1/auth/login", json=payload, timeout=10.0)
                
                if response.status_code == 200:
                    data = response.json()
                    token = data.get("access_token")
                    if token:
                        return True, "Login successful", token
                    return False, "Invalid response from server", None
                else:
                    error_msg = response.json().get("detail", "Authentication failed")
                    return False, error_msg, None
                    
        except httpx.RequestError as e:
            logger.error(f"Network error during login: {e}")
            return False, "Could not connect to authentication server. Check your internet connection.", None
        except Exception as e:
            logger.error(f"Unexpected error during login: {e}")
            return False, "An unexpected error occurred.", None
