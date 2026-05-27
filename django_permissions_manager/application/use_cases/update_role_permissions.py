from typing import List
from ..dto.role_dto import RoleDTO
from ...domain.repositories.role_repository import RoleRepository
from ...domain.repositories.permission_repository import PermissionRepository
from ...domain.value_objects.permission_code import PermissionCode

class UpdateRolePermissionsUseCase:
    """Application use case for updating the permissions of a role."""

    def __init__(
        self,
        role_repository: RoleRepository,
        permission_repository: PermissionRepository
    ):
        """Initializes the use case.

        Args:
            role_repository: The role repository.
            permission_repository: The permission repository.
        """
        self.role_repository = role_repository
        self.permission_repository = permission_repository

    def execute(self, role_id: str, permission_codes: List[str]) -> RoleDTO:
        """Updates the list of permissions associated with a role.

        Args:
            role_id: The ID of the role to update.
            permission_codes: List of strings representing the new permission codes.

        Returns:
            RoleDTO: The updated role data.

        Raises:
            ValueError: If the role is not found.
        """
        # 1. Fetch the role
        role = self.role_repository.get_by_id(role_id)
        if not role:
            raise ValueError(f"Role {role_id} not found.")

        # 2. Resolve permission objects from codes
        new_permissions = []
        for code in permission_codes:
            perm = self.permission_repository.get_by_code(PermissionCode(code))
            if perm:
                new_permissions.append(perm)

        # 3. Update the domain entity
        role.permissions = new_permissions
        
        # 4. Persist changes
        self.role_repository.save(role)

        # 5. Return updated DTO
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
            updated_at=role.updated_at
        )
