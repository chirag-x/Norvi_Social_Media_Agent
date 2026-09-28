import keyring
from typing import Optional
from src.utils.logger import logger

SERVICE_NAME = "norvi_social_media_agent"
TOKEN_KEY = "access_token"

class SessionManager:
    """
    Manages the user's active session securely using the OS credential store.
    """
    
    @staticmethod
    def save_token(token: str) -> bool:
        """Saves the access token securely."""
        try:
            keyring.set_password(SERVICE_NAME, TOKEN_KEY, token)
            logger.info("Session token saved securely.")
            return True
        except Exception as e:
            logger.error(f"Failed to save session token: {e}")
            return False

    @staticmethod
    def get_token() -> Optional[str]:
        """Retrieves the saved access token, if any."""
        try:
            return keyring.get_password(SERVICE_NAME, TOKEN_KEY)
        except Exception as e:
            logger.error(f"Failed to retrieve session token: {e}")
            return None

    @staticmethod
    def clear_session() -> bool:
        """Deletes the saved access token (logout)."""
        try:
            keyring.delete_password(SERVICE_NAME, TOKEN_KEY)
            logger.info("Session token cleared.")
            return True
        except keyring.errors.PasswordDeleteError:
            # Token was already gone, that's fine
            return True
        except Exception as e:
            logger.error(f"Failed to clear session token: {e}")
            return False

    @staticmethod
    def is_authenticated() -> bool:
        """Checks if a valid token exists."""
        return SessionManager.get_token() is not None
