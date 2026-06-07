import abc
from typing import List, Optional

from ..entities.permission import Permission
from ..value_objects.permission_code import PermissionCode


class PermissionReadRepository(abc.ABC):
    """Read-only port for querying permissions.

    Use cases that only need to look up permissions depend on this interface,
    keeping their dependencies minimal (Interface Segregation Principle).
    """

    @abc.abstractmethod
    def get_by_id(self, permission_id: str) -> Optional[Permission]:
        """Retrieves a permission by its integer ID."""

    @abc.abstractmethod
    def get_by_code(self, code: PermissionCode) -> Optional[Permission]:
        """Retrieves a permission by its unique 'app_label.codename' code."""

    @abc.abstractmethod
    def get_all(self) -> List[Permission]:
        """Retrieves all available permissions."""
