from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class Project(BaseModel):
    """
    Domain model for a user's workspace or project.
    """
    id: str
    user_id: str
    name: str
    description: Optional[str] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
