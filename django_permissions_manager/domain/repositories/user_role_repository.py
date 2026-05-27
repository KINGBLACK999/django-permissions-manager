import abc
from typing import List, Optional
from ..entities.user_role import UserRole
from ..value_objects.user_id import UserId

class UserRoleRepository(abc.ABC):
    """Abstract interface (Port) for UserRole assignment persistence."""
    
    @abc.abstractmethod
    def save(self, user_role: UserRole) -> None:
        """Saves a user-role assignment."""
        pass

    @abc.abstractmethod
    def get_by_id(self, user_role_id: str) -> Optional[UserRole]:
        """Retrieves an assignment by ID."""
        pass

    @abc.abstractmethod
    def get_by_user_id(self, user_id: UserId) -> List[UserRole]:
        """Retrieves all role assignments for a specific user."""
        pass

    @abc.abstractmethod
    def get_by_role_id(self, role_id: str) -> List[UserRole]:
        """Retrieves all user assignments for a specific role."""
        pass

    @abc.abstractmethod
    def delete(self, user_role_id: str) -> None:
        """Deletes an assignment by ID."""
        pass
