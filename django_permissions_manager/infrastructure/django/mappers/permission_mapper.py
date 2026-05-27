from django.contrib.auth.models import Permission as DjangoPermission
from ....domain.entities.permission import Permission
from ....domain.value_objects.permission_code import PermissionCode

class PermissionMapper:
    """Mapper between Django Permission model and Domain Permission entity."""

    @staticmethod
    def to_domain(orm_model: DjangoPermission) -> Permission:
        """Converts a Django Permission model to a Domain Permission entity."""
        # Using app_label.codename as the unique permission code
        code = f"{orm_model.content_type.app_label}.{orm_model.codename}"
        
        return Permission(
            id=str(orm_model.id),
            code=PermissionCode(code),
            name=orm_model.name,
            content_type=orm_model.content_type.model
        )
