import uuid
from typing import List, Optional
from dataclasses import dataclass

from ...domain.entities.permission_group import PermissionGroup
from ...domain.repositories.permission_group_repository import PermissionGroupRepository
from ...domain.repositories.permission_repository import PermissionRepository
from ...domain.value_objects.permission_code import PermissionCode


@dataclass(frozen=True)
class PermissionGroupDTO:
    id: str
    name: str
    description: str
    permissions: List[str]


class CreatePermissionGroupUseCase:
    """Creates a named group of permissions that can be bulk-assigned to a role."""

    def __init__(
        self,
        group_repository: PermissionGroupRepository,
        permission_repository: PermissionRepository,
    ):
        self.group_repository = group_repository
        self.permission_repository = permission_repository

    def execute(
        self,
        name: str,
        description: str = "",
        permission_codes: Optional[List[str]] = None,
    ) -> PermissionGroupDTO:
        """Creates a permission group.

        Args:
            name: Unique name for the group.
            description: Optional description.
            permission_codes: List of 'app_label.codename' codes.

        Raises:
            ValueError: If a group with the same name already exists.
        """
        if self.group_repository.get_by_name(name):
            raise ValueError(f"Permission group '{name}' already exists.")

        permissions = []
        if permission_codes:
            for code in permission_codes:
                perm = self.permission_repository.get_by_code(PermissionCode(code))
                if perm:
                    permissions.append(perm)

        group = PermissionGroup(
            id=str(uuid.uuid4()),
            name=name,
            description=description,
            permissions=permissions,
        )
        self.group_repository.save(group)

        return PermissionGroupDTO(
            id=group.id,
            name=group.name,
            description=group.description,
            permissions=[p.code.value for p in group.permissions],
        )
