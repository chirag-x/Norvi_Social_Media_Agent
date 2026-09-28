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
        self._db_path = data_dir / "norvi_local.db"
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
