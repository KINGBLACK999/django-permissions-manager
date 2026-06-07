import abc

from ..entities.permission import Permission
from .permission_read_repository import PermissionReadRepository


class PermissionRepository(PermissionReadRepository):
    """Full CRUD port for Permission persistence.

    Extends the read-only interface with write capability.
    Use this when an adapter needs to create permissions programmatically
    (e.g. a custom backend that doesn't rely on Django migrations).

    Note: The built-in Django adapter (DjangoPermissionRepository) intentionally
    implements only PermissionReadRepository, because Django generates permissions
    automatically via the migration system.
    """

    @abc.abstractmethod
    def save(self, permission: Permission) -> None:
        """Persists a permission entity."""
