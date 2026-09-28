import os
from pathlib import Path
from src.storage.database.database import DatabaseManager
from src.utils.logger import logger

class MigrationManager:
    """
    Handles creating and updating the local SQLite database schema.
    """
    def __init__(self):
        self.db = DatabaseManager.get_instance()
        self.schemas_dir = Path(__file__).parent / "schemas"

    def initialize_migrations_table(self):
        """Ensures the migrations tracking table exists."""
        with self.db.get_connection() as conn:
            conn.execute("""
                CREATE TABLE IF NOT EXISTS _migrations (
                    version INTEGER PRIMARY KEY,
                    name TEXT NOT NULL,
                    applied_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)
            conn.commit()

    def get_applied_migrations(self):
        """Returns a list of applied migration versions."""
        with self.db.get_connection() as conn:
            cursor = conn.execute("SELECT version FROM _migrations ORDER BY version ASC")
            return [row["version"] for row in cursor.fetchall()]

    def apply_migrations(self):
        """Finds and applies pending SQL schema files in order."""
        self.initialize_migrations_table()
        applied = self.get_applied_migrations()
        
        # Get all .sql files in the schemas directory
        if not self.schemas_dir.exists():
            logger.warning(f"Schemas directory not found: {self.schemas_dir}")
            return
            
        sql_files = sorted([f for f in os.listdir(self.schemas_dir) if f.endswith(".sql")])
        
        for file_name in sql_files:
            try:
                version = int(file_name.split("_")[0])
            except ValueError:
                logger.error(f"Invalid migration file name format: {file_name}")
                continue
                
            if version not in applied:
                self._apply_file(version, file_name)

    def _apply_file(self, version: int, file_name: str):
        file_path = self.schemas_dir / file_name
        logger.info(f"Applying migration {file_name}...")
        
        with open(file_path, "r", encoding="utf-8") as f:
            sql_script = f.read()
            
        try:
            with self.db.get_connection() as conn:
                conn.executescript(sql_script)
                conn.execute(
                    "INSERT INTO _migrations (version, name) VALUES (?, ?)", 
                    (version, file_name)
                )
                conn.commit()
            logger.info(f"Successfully applied migration {file_name}")
        except Exception as e:
            logger.error(f"Failed to apply migration {file_name}: {e}")
            raise
