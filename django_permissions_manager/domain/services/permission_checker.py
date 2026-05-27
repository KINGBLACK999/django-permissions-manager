from typing import List
from ..entities.user_role import UserRole

class PermissionChecker:
    """Domain service to check user permissions across multiple roles."""
    
    @staticmethod
    def has_permission(user_roles: List[UserRole], permission_code: str) -> bool:
        """Checks if any active user role grants the specified permission.

        Args:
            user_roles: List of UserRole assignments for a user.
            permission_code: The code of the permission to verify.

        Returns:
            bool: True if access is granted.
        """
        for user_role in user_roles:
            if user_role.role.is_active and user_role.role.has_permission(permission_code):
                return True
        return False

    @classmethod
    def has_any_permission(cls, user_roles: List[UserRole], permission_codes: List[str]) -> bool:
        """Checks if the user has at least one of the provided permissions."""
        return any(cls.has_permission(user_roles, code) for code in permission_codes)

    @classmethod
    def has_all_permissions(cls, user_roles: List[UserRole], permission_codes: List[str]) -> bool:
        """Checks if the user has all of the provided permissions."""
        return all(cls.has_permission(user_roles, code) for code in permission_codes)
