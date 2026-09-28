import json
import uuid
from typing import Optional
from datetime import datetime

from src.storage.database.database import DatabaseManager
from src.domain.models.profile import UserProfile

class UserDAO:
    """
    Data Access Object for UserProfile.
    """
    def __init__(self):
        self.db = DatabaseManager.get_instance()

    def create_or_update(self, email: str) -> UserProfile:
        """
        Creates a new user profile or updates the last_login of an existing one.
        """
        existing = self.get_by_email(email)
        now = datetime.utcnow().isoformat()
        
        with self.db.get_connection() as conn:
            if existing:
                conn.execute(
                    "UPDATE user_profiles SET last_login = ? WHERE email = ?",
                    (now, email)
                )
                conn.commit()
                existing.last_login = datetime.fromisoformat(now)
                return existing
            else:
                new_id = str(uuid.uuid4())
                conn.execute(
                    "INSERT INTO user_profiles (id, email, created_at, last_login, settings) VALUES (?, ?, ?, ?, ?)",
                    (new_id, email, now, now, "{}")
                )
                conn.commit()
                return UserProfile(
                    id=new_id,
                    email=email,
                    created_at=datetime.fromisoformat(now),
                    last_login=datetime.fromisoformat(now)
                )

    def get_by_email(self, email: str) -> Optional[UserProfile]:
        with self.db.get_connection() as conn:
            cursor = conn.execute("SELECT * FROM user_profiles WHERE email = ?", (email,))
            row = cursor.fetchone()
            
            if row:
                return UserProfile(
                    id=row["id"],
                    email=row["email"],
                    created_at=datetime.fromisoformat(row["created_at"]) if row["created_at"] else None,
                    last_login=datetime.fromisoformat(row["last_login"]) if row["last_login"] else None,
                    settings=json.loads(row["settings"]) if row["settings"] else {}
                )
        return None
