from dataclasses import dataclass
from typing import List, Optional
from datetime import datetime

@dataclass(frozen=True)
class RoleDTO:
    """Data Transfer Object for Role data."""
    id: str
    name: str
    description: str
    entity_type: Optional[str]
    entity_id: Optional[str]
    permissions: List[str]  # List of permission codes
    is_active: bool
    is_system_role: bool
    created_at: datetime
    updated_at: datetime
