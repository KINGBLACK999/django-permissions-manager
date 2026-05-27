from typing import List, Optional
from ....domain.entities.user_role import UserRole
from ....domain.repositories.user_role_repository import UserRoleRepository
from ....domain.value_objects.user_id import UserId
from ..models.user_role_model import UserRoleModel
from ..mappers.user_role_mapper import UserRoleMapper

class DjangoUserRoleRepository(UserRoleRepository):
    """Django implementation of the UserRoleRepository interface."""

    def save(self, user_role: UserRole) -> None:
        """Saves a User-Role assignment."""
        UserRoleModel.objects.update_or_create(
            id=user_role.id,
            defaults={
                'user_id': int(user_role.user_id.value),
                'role_id': user_role.role.id,
                'assigned_by_id': int(user_role.assigned_by.value) if user_role.assigned_by else None
            }
        )

    def get_by_id(self, user_role_id: str) -> Optional[UserRole]:
        """Retrieves an assignment by UUID."""
        try:
            orm_ur = UserRoleModel.objects.select_related('role').get(id=user_role_id)
            return UserRoleMapper.to_domain(orm_ur)
        except UserRoleModel.DoesNotExist:
            return None

    def get_by_user_id(self, user_id: UserId) -> List[UserRole]:
        """Retrieves all role assignments for a user."""
        orm_assignments = UserRoleModel.objects.select_related(
            'role'
        ).prefetch_related(
            'role__permissions__content_type'
        ).filter(user_id=user_id.value)
        
        return [UserRoleMapper.to_domain(ur) for ur in orm_assignments]

    def get_by_role_id(self, role_id: str) -> List[UserRole]:
        """Retrieves all user assignments for a specific role."""
        orm_assignments = UserRoleModel.objects.select_related(
            'role'
        ).prefetch_related(
            'role__permissions__content_type'
        ).filter(role_id=role_id)
        return [UserRoleMapper.to_domain(ur) for ur in orm_assignments]

    def delete(self, user_role_id: str) -> None:
        """Deletes an assignment."""
        UserRoleModel.objects.filter(id=user_role_id).delete()
