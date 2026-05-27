from typing import List, Optional
from django.contrib.auth.models import Permission as DjangoPermission
from ....domain.entities.permission import Permission
from ....domain.repositories.permission_repository import PermissionRepository
from ....domain.value_objects.permission_code import PermissionCode
from ..mappers.permission_mapper import PermissionMapper

class DjangoPermissionRepository(PermissionRepository):
    """Django implementation of the PermissionRepository interface."""

    def save(self, permission: Permission) -> None:
        """Saves a permission (usually permissions are managed by Django content types)."""
        # In a typical Django app, permissions are created via migrations/signals.
        # This is a basic implementation.
        pass

    def get_by_id(self, permission_id: str) -> Optional[Permission]:
        """Retrieves a permission by its integer ID."""
        try:
            orm_permission = DjangoPermission.objects.select_related('content_type').get(id=permission_id)
            return PermissionMapper.to_domain(orm_permission)
        except DjangoPermission.DoesNotExist:
            return None

    def get_by_code(self, code: PermissionCode) -> Optional[Permission]:
        """Retrieves a permission by its 'app_label.codename'."""
        try:
            app_label, codename = code.value.split('.')
            orm_permission = DjangoPermission.objects.select_related('content_type').get(
                content_type__app_label=app_label,
                codename=codename
            )
            return PermissionMapper.to_domain(orm_permission)
        except (DjangoPermission.DoesNotExist, ValueError):
            return None

    def get_all(self) -> List[Permission]:
        """Retrieves all available permissions in the Django system."""
        orm_permissions = DjangoPermission.objects.select_related('content_type').all()
        return [PermissionMapper.to_domain(p) for p in orm_permissions]
