from dataclasses import dataclass
from datetime import datetime
from typing import Optional

from ..value_objects.user_id import UserId
from .role import Role

@dataclass
class UserRole:
    """Domain entity representing the assignment of a role to a user."""
    id: str
    user_id: UserId
    role: Role
    assigned_at: datetime
    assigned_by: Optional[UserId]

    def validate(self) -> None:
        """Performs business validation for the assignment."""
        pass
