from pydantic import BaseModel, EmailStr
from typing import Optional, Dict, Any
from datetime import datetime

class UserProfile(BaseModel):
    """
    Domain model for a local user profile.
    """
    id: str
    email: EmailStr
    created_at: Optional[datetime] = None
    last_login: Optional[datetime] = None
    settings: Dict[str, Any] = {}
