import uuid
from datetime import datetime, timezone
from typing import List, Optional

from ..entities.role import Role
from ..entities.permission import Permission
from ..value_objects.role_name import RoleName
from ..value_objects.entity_reference import EntityReference

class RoleFactory:
    """Factory service for creating Role entities."""
    
    @staticmethod
    def create_role(
        name: str,
        description: str = "",
        entity_reference: Optional[EntityReference] = None,
        permissions: Optional[List[Permission]] = None,
        is_system_role: bool = False
    ) -> Role:
        """Creates a new Role entity with properly initialized values.

        Args:
            name: Display name for the role.
            description: Optional detailed description.
            entity_reference: Reference to the entity scope (optional).
            permissions: List of initial permissions (optional).
            is_system_role: If True, the role cannot be deleted or deactivated.

        Returns:
            Role: A new instance of a Role entity.
        """
        now = datetime.now(timezone.utc)
        return Role(
            id=str(uuid.uuid4()),
            name=RoleName(name),
            description=description,
            entity_reference=entity_reference,
            permissions=permissions or [],
            is_active=True,
            is_system_role=is_system_role,
            created_at=now,
            updated_at=now
        )
