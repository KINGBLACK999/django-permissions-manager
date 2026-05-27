from dataclasses import dataclass, field
from typing import List
from .permission import Permission

@dataclass
class PermissionGroup:
    """Domain entity representing a logical group of permissions."""
    id: str
    name: str
    description: str
    permissions: List[Permission] = field(default_factory=list)
