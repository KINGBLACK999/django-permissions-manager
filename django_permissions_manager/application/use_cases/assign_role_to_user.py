import uuid
from datetime import datetime, timezone
from typing import Callable, Optional

from ..dto.user_role_dto import UserRoleDTO
from ...domain.entities.user_role import UserRole
from ...domain.repositories.user_role_repository import UserRoleRepository
from ...domain.repositories.role_repository import RoleRepository
from ...domain.value_objects.user_id import UserId


class AssignRoleToUserUseCase:
    """Application use case for assigning a role to a user.

    Attributes:
        user_role_repository (UserRoleRepository): Repository for user-role assignments.
        role_repository (RoleRepository): Repository for role entities.
        on_assigned (Callable, optional): Callback invoked after a role is assigned.
            Receives keyword arguments ``user_id``, ``role_id``, and ``assigned_by``.
            Injected by the infrastructure layer (e.g. a Django signal).
    """
    def __init__(
        self,
        user_role_repository: UserRoleRepository,
        role_repository: RoleRepository,
        on_assigned: Optional[Callable[..., None]] = None,
    ):
        """Initializes the use case.

        Args:
            user_role_repository: The user role repository.
            role_repository: The role repository.
            on_assigned: Optional callback fired after a successful assignment.
        """
        self.user_role_repository = user_role_repository
        self.role_repository = role_repository
        self.on_assigned = on_assigned

    def execute(
        self,
        user_id: str,
        role_id: str,
        assigned_by_id: Optional[str] = None
    ) -> UserRoleDTO:
        """Assigns a role to a user.

        Args:
            user_id: The ID of the user.
            role_id: The ID of the role to assign.
            assigned_by_id: Optional ID of the user making the assignment.

        Returns:
            UserRoleDTO: The created assignment data.

        Raises:
            ValueError: If the role does not exist.
        """

        # 1. Fetch the role
        role = self.role_repository.get_by_id(role_id)
        if not role:
            raise ValueError(f"Role with id '{role_id}' does not exist.")

        # 2. Build domain entity
        user_role = UserRole(
            id=str(uuid.uuid4()),
            user_id=UserId(user_id),
            role=role,
            assigned_at=datetime.now(timezone.utc),
            assigned_by=UserId(assigned_by_id) if assigned_by_id else None
        )

        # 3. Persist
        self.user_role_repository.save(user_role)

        # 4. Notify via callback (injected by infrastructure layer)
        if self.on_assigned:
            self.on_assigned(
                user_id=user_id,
                role_id=role_id,
                assigned_by=assigned_by_id,
            )

        # 5. Return DTO
        return UserRoleDTO(
            id=user_role.id,
            user_id=user_role.user_id.value,
            role_id=role.id,
            role_name=role.name.value,
            assigned_at=user_role.assigned_at,
            assigned_by=user_role.assigned_by.value if user_role.assigned_by else None
        )
