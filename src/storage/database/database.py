import sqlite3
import os
from pathlib import Path
from src.config.config import get_config
from src.utils.logger import logger

class DatabaseManager:
    """
    Manages the local SQLite database connection.
    Ensures that all user data remains strictly on the local filesystem.
    """
    _instance = None
    _db_path = None

    @classmethod
    def get_instance(cls):
        if cls._instance is None:
            cls._instance = DatabaseManager()
        return cls._instance

    def __init__(self):
        config = get_config()
        
        # Ensure app_data directory exists
        data_dir = Path(config.app_data_dir)
        data_dir.mkdir(parents=True, exist_ok=True)
        
        # Define DB path
        self._db_path = data_dir / "nexus_local.db"
        logger.info(f"Database initialized at: {self._db_path}")

    def get_connection(self) -> sqlite3.Connection:
        """
        Returns a configured SQLite connection.
        Enables foreign keys and returns dictionary-like rows.
        """
        conn = sqlite3.connect(self._db_path)
        conn.row_factory = sqlite3.Row
        conn.execute("PRAGMA foreign_keys = ON;")
        return conn

    # ------------------------------------------------------------------
    # Secure API Key Storage (Phase 26/27 Token Encryption)
    # ------------------------------------------------------------------
    def get_api_keys(self, platform: str) -> dict:
        """Returns API keys decrypted on the fly."""
        from src.storage.security.crypto import CryptoManager
        with self.get_connection() as conn:
            cursor = conn.execute("SELECT * FROM api_keys WHERE platform = ?", (platform,))
            row = cursor.fetchone()
            
        if not row:
            return {}
            
        return {
            "platform": row["platform"],
            "client_id": CryptoManager.decrypt(row["client_id"]),
            "client_secret": CryptoManager.decrypt(row["client_secret"]),
            "access_token": CryptoManager.decrypt(row["access_token"]),
            "refresh_token": CryptoManager.decrypt(row["refresh_token"])
        }
        
    def update_api_keys(self, platform: str, refresh_token: str):
        """Updates only the refresh_token (encrypted). Used by auto-refresh API calls."""
        from src.storage.security.crypto import CryptoManager
        enc_token = CryptoManager.encrypt(refresh_token)
        with self.get_connection() as conn:
            conn.execute("UPDATE api_keys SET refresh_token = ? WHERE platform = ?", (enc_token, platform))
            conn.commit()

    # ------------------------------------------------------------------
    # App Settings (Phase 28)
    # ------------------------------------------------------------------
    def get_setting(self, key: str, default: str = "") -> str:
        with self.get_connection() as conn:
            try:
                cursor = conn.execute("SELECT value FROM app_settings WHERE key = ?", (key,))
                row = cursor.fetchone()
                if row:
                    return row["value"]
            except Exception:
                pass
        return default

    def set_setting(self, key: str, value: str):
        with self.get_connection() as conn:
            try:
                conn.execute(
                    "INSERT INTO app_settings (key, value) VALUES (?, ?) ON CONFLICT(key) DO UPDATE SET value=excluded.value",
                    (key, value)
                )
                conn.commit()
            except Exception as e:
                logger.error(f"Failed to save setting {key}: {e}")
