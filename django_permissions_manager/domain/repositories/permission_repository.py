import abc
from typing import List, Optional
from ..entities.permission import Permission
from ..value_objects.permission_code import PermissionCode

class PermissionRepository(abc.ABC):
    """Abstract interface (Port) for Permission persistence."""
    
    @abc.abstractmethod
    def save(self, permission: Permission) -> None:
        """Saves a permission entity."""
        pass

    @abc.abstractmethod
    def get_by_id(self, permission_id: str) -> Optional[Permission]:
        """Retrieves a permission by ID."""
        pass

    @abc.abstractmethod
    def get_by_code(self, code: PermissionCode) -> Optional[Permission]:
        """Retrieves a permission by its unique code."""
        pass

    @abc.abstractmethod
    def get_all(self) -> List[Permission]:
        """Retrieves all permissions."""
        pass
