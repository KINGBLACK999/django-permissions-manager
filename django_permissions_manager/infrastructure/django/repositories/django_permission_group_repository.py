import uuid
from typing import List, Optional

from ....domain.entities.permission_group import PermissionGroup
from ....domain.repositories.permission_group_repository import PermissionGroupRepository
from ..models.permission_group_model import PermissionGroupModel
from ..mappers.permission_group_mapper import PermissionGroupMapper


class DjangoPermissionGroupRepository(PermissionGroupRepository):
    """Django implementation of the PermissionGroupRepository interface."""

    def save(self, group: PermissionGroup) -> None:
        orm_group, _ = PermissionGroupModel.objects.update_or_create(
            id=group.id,
            defaults={
                'name': group.name,
                'description': group.description,
            }
        )
        permission_ids = [int(p.id) for p in group.permissions]
        orm_group.permissions.set(permission_ids)

    def get_by_id(self, group_id: str) -> Optional[PermissionGroup]:
        try:
            orm_group = PermissionGroupModel.objects.prefetch_related(
                'permissions__content_type'
            ).get(id=group_id)
            return PermissionGroupMapper.to_domain(orm_group)
        except PermissionGroupModel.DoesNotExist:
            return None

    def get_by_name(self, name: str) -> Optional[PermissionGroup]:
        try:
            orm_group = PermissionGroupModel.objects.prefetch_related(
                'permissions__content_type'
            ).get(name=name)
            return PermissionGroupMapper.to_domain(orm_group)
        except PermissionGroupModel.DoesNotExist:
            return None

    def get_all(self) -> List[PermissionGroup]:
        orm_groups = PermissionGroupModel.objects.prefetch_related(
            'permissions__content_type'
        ).all()
        return [PermissionGroupMapper.to_domain(g) for g in orm_groups]

    def delete(self, group_id: str) -> None:
        PermissionGroupModel.objects.filter(id=group_id).delete()
