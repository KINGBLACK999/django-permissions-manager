from dataclasses import dataclass, field
from datetime import datetime
from typing import List, Optional

from ..value_objects.role_name import RoleName
from ..value_objects.entity_reference import EntityReference
from .permission import Permission

@dataclass
class Role:
    """Domain entity representing a Role.

    Roles can be global or scoped to a specific entity (e.g., a Company).
    """
    id: str
    name: RoleName
    description: str
    entity_reference: Optional[EntityReference]
    permissions: List[Permission]
    is_active: bool
    is_system_role: bool
    created_at: datetime
    updated_at: datetime

    def is_global(self) -> bool:
        """Checks if the role is global (not scoped to any entity)."""
        return self.entity_reference is None

    def add_permission(self, permission: Permission) -> None:
        """Adds a permission to the role if not already present."""
        if not any(p.id == permission.id for p in self.permissions):
            self.permissions.append(permission)

    def remove_permission(self, permission: Permission) -> None:
        """Removes a permission from the role."""
        self.permissions = [p for p in self.permissions if p.id != permission.id]

    def has_permission(self, permission_code: str) -> bool:
        """Checks if the role grants a specific permission code."""
        return any(p.matches(permission_code) for p in self.permissions)

    def validate(self) -> None:
        """Performs domain business validations."""
        pass

    def can_be_deleted(self) -> bool:
        """Checks if the role is allowed to be deleted (system roles are not)."""
        return not self.is_system_role
