from typing import Optional
from datetime import datetime

class UserDocument:
    """MongoDB document structure for users"""
    def __init__(self, id: str, name: str, phone: str, created_at: Optional[datetime] = None):
        self.id = id
        self.name = name
        self.phone = phone
        self.created_at = created_at or datetime.utcnow()
    
    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "phone": self.phone,
            "created_at": self.created_at
        }