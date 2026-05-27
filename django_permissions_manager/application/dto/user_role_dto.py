from dataclasses import dataclass
from datetime import datetime
from typing import Optional

@dataclass(frozen=True)
class UserRoleDTO:
    """Data Transfer Object for User-Role assignment data."""
    id: str
    user_id: str
    role_id: str
    role_name: str
    assigned_at: datetime
    assigned_by: Optional[str]
