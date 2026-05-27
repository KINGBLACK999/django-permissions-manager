from ..models.permission_group_model import PermissionGroupModel
from ....domain.entities.permission_group import PermissionGroup
from .permission_mapper import PermissionMapper


class PermissionGroupMapper:
    """Mapper between PermissionGroupModel and PermissionGroup domain entity."""

    @staticmethod
    def to_domain(orm_model: PermissionGroupModel) -> PermissionGroup:
        return PermissionGroup(
            id=str(orm_model.id),
            name=orm_model.name,
            description=orm_model.description,
            permissions=[PermissionMapper.to_domain(p) for p in orm_model.permissions.all()],
        )
