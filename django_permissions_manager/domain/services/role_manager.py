from datetime import datetime, timezone
from typing import Optional

from ..entities.role import Role
from ..repositories.role_repository import RoleRepository
from ..value_objects.entity_reference import EntityReference
from ..exceptions.role_exceptions import SystemRoleDeletionException, RoleAlreadyExistsException
from ...infrastructure.django.signals import role_status_changed

class RoleManager:
    """Domain service for managing role-related business logic.

    This service handles operations that involve validations against the repository
    or business rules spanning multiple entities.

    Attributes:
        role_repository (RoleRepository): The repository for role persistence.
    """
    def __init__(self, role_repository: RoleRepository):
        """Initializes the RoleManager.

        Args:
            role_repository: An implementation of the RoleRepository interface.
        """
        self.role_repository = role_repository

    def deactivate_role(self, role: Role) -> None:
        """Deactivates a role if it's not a system role.

        Args:
            role: The role entity to deactivate.

        Raises:
            SystemRoleDeletionException: If the role is marked as a system role.
        """
        if role.is_system_role:
            raise SystemRoleDeletionException("System roles cannot be deactivated.")
        
        role.is_active = False
        role.updated_at = datetime.now(timezone.utc)
        self.role_repository.save(role)
        role_status_changed.send(sender=self.__class__, role_id=role.id, is_active=False)

    def activate_role(self, role: Role) -> None:
        """Activates a role.

        Args:
            role: The role entity to activate.
        """
        role.is_active = True
        role.updated_at = datetime.now(timezone.utc)
        self.role_repository.save(role)
        role_status_changed.send(sender=self.__class__, role_id=role.id, is_active=True)

    def ensure_role_name_is_unique(self, name: str, entity_reference: Optional[EntityReference] = None) -> None:
        """Ensures that a role name is unique within its scope.

        Args:
            name: The name of the role to check.
            entity_reference: Optional reference to the entity scope (e.g., Company).
                If None, checks in the global scope.

        Raises:
            RoleAlreadyExistsException: If a role with the same name exists in the same scope.
        """
        existing_role = self.role_repository.get_by_name(name, entity_reference)
        if existing_role:
            scope = "global" if entity_reference is None else f"for entity {entity_reference.entity_type}:{entity_reference.entity_id}"
            raise RoleAlreadyExistsException(f"A role with the name '{name}' already exists ({scope}).")
