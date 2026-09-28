import uuid
from typing import List, Optional
from datetime import datetime

from src.storage.database.database import DatabaseManager
from src.domain.models.project import Project

class ProjectDAO:
    """
    Data Access Object for Projects.
    """
    def __init__(self):
        self.db = DatabaseManager.get_instance()

    def create(self, user_id: str, name: str, description: Optional[str] = None) -> Project:
        now = datetime.utcnow().isoformat()
        new_id = str(uuid.uuid4())
        
        with self.db.get_connection() as conn:
            conn.execute(
                "INSERT INTO projects (id, user_id, name, description, created_at, updated_at) VALUES (?, ?, ?, ?, ?, ?)",
                (new_id, user_id, name, description, now, now)
            )
            conn.commit()
            
        return Project(
            id=new_id,
            user_id=user_id,
            name=name,
            description=description,
            created_at=datetime.fromisoformat(now),
            updated_at=datetime.fromisoformat(now)
        )

    def get_by_user(self, user_id: str) -> List[Project]:
        with self.db.get_connection() as conn:
            cursor = conn.execute("SELECT * FROM projects WHERE user_id = ? ORDER BY updated_at DESC", (user_id,))
            rows = cursor.fetchall()
            
            projects = []
            for row in rows:
                projects.append(Project(
                    id=row["id"],
                    user_id=row["user_id"],
                    name=row["name"],
                    description=row["description"],
                    created_at=datetime.fromisoformat(row["created_at"]) if row["created_at"] else None,
                    updated_at=datetime.fromisoformat(row["updated_at"]) if row["updated_at"] else None
                ))
            return projects
