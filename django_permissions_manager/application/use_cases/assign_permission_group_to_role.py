from ...domain.repositories.permission_group_repository import PermissionGroupRepository
from ...domain.repositories.role_repository import RoleRepository
from ..dto.role_dto import RoleDTO


class AssignPermissionGroupToRoleUseCase:
    """Adds all permissions from a group into a role (bulk assignment)."""

    def __init__(
        self,
        role_repository: RoleRepository,
        group_repository: PermissionGroupRepository,
    ):
        self.role_repository = role_repository
        self.group_repository = group_repository

    def execute(self, role_id: str, group_id: str) -> RoleDTO:
        """Merges the group's permissions into the role.

        Args:
            role_id: UUID of the target role.
            group_id: UUID of the permission group.

        Raises:
            ValueError: If either the role or the group does not exist.
        """
        role = self.role_repository.get_by_id(role_id)
        if not role:
            raise ValueError(f"Role '{role_id}' does not exist.")

        group = self.group_repository.get_by_id(group_id)
        if not group:
            raise ValueError(f"Permission group '{group_id}' does not exist.")

        for permission in group.permissions:
            role.add_permission(permission)

        self.role_repository.save(role)

        return RoleDTO(
            id=role.id,
            name=role.name.value,
            description=role.description,
            entity_type=role.entity_reference.entity_type if role.entity_reference else None,
            entity_id=role.entity_reference.entity_id if role.entity_reference else None,
            permissions=[p.code.value for p in role.permissions],
            is_active=role.is_active,
            is_system_role=role.is_system_role,
            created_at=role.created_at,
            updated_at=role.updated_at,
        )
