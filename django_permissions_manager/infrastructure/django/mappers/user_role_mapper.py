from ..models.user_role_model import UserRoleModel
from ....domain.entities.user_role import UserRole
from ....domain.value_objects.user_id import UserId
from .role_mapper import RoleMapper

class UserRoleMapper:
    """Mapper between UserRoleModel and UserRole domain entity."""

    @staticmethod
    def to_domain(orm_model: UserRoleModel) -> UserRole:
        """Maps an ORM model to a Domain entity."""
        return UserRole(
            id=str(orm_model.id),
            user_id=UserId(str(orm_model.user_id)),
            role=RoleMapper.to_domain(orm_model.role),
            assigned_at=orm_model.assigned_at,
            assigned_by=UserId(str(orm_model.assigned_by_id)) if orm_model.assigned_by_id else None
        )
