from typing import List

from ..dto.user_role_dto import UserRoleDTO
from ...domain.repositories.user_role_repository import UserRoleRepository
from ...domain.value_objects.user_id import UserId

class GetUserRolesUseCase:
    """Application use case for retrieving a user's assigned roles."""

    def __init__(self, user_role_repository: UserRoleRepository):
        """Initializes the use case.

        Args:
            user_role_repository: The user role repository.
        """
        self.user_role_repository = user_role_repository

    def execute(self, user_id: str) -> List[UserRoleDTO]:
        """Retrieves all roles assigned to a user.

        Args:
            user_id: The ID of the user.

        Returns:
            List[UserRoleDTO]: A list of user-role assignment DTOs.
        """
        user_roles = self.user_role_repository.get_by_user_id(UserId(user_id))
        
        return [
            UserRoleDTO(
                id=ur.id,
                user_id=ur.user_id.value,
                role_id=ur.role.id,
                role_name=ur.role.name.value,
                assigned_at=ur.assigned_at,
                assigned_by=ur.assigned_by.value if ur.assigned_by else None
            )
            for ur in user_roles
        ]
