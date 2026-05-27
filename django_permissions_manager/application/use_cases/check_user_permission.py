from ...domain.repositories.user_role_repository import UserRoleRepository
from ...domain.services.permission_checker import PermissionChecker
from ...domain.value_objects.user_id import UserId

class CheckUserPermissionUseCase:
    """Application use case for verifying if a user has a specific permission."""

    def __init__(
        self,
        user_role_repository: UserRoleRepository,
        permission_checker: PermissionChecker
    ):
        """Initializes the use case.

        Args:
            user_role_repository: The user role repository.
            permission_checker: The permission checker service.
        """
        self.user_role_repository = user_role_repository
        self.permission_checker = permission_checker

    def execute(self, user_id: str, permission_code: str) -> bool:
        """Verifies if the user has the given permission.

        Args:
            user_id: The ID of the user.
            permission_code: The code of the permission to check.

        Returns:
            bool: True if the user has the permission, False otherwise.
        """
        # 1. Fetch user roles from the repository
        user_roles = self.user_role_repository.get_by_user_id(UserId(user_id))

        # 2. Delegate verification logic to the domain service
        return self.permission_checker.has_permission(user_roles, permission_code)
