from typing import List, Optional
from ....domain.entities.role import Role
from ....domain.repositories.role_repository import RoleRepository
from ....domain.value_objects.entity_reference import EntityReference
from ..models.role_model import RoleModel
from ..mappers.role_mapper import RoleMapper

class DjangoRoleRepository(RoleRepository):
    """Django implementation of the RoleRepository interface."""

    def save(self, role: Role) -> None:
        """Saves or updates a Role in the Django database."""
        orm_role, _ = RoleModel.objects.update_or_create(
            id=role.id,
            defaults={
                'name': role.name.value,
                'description': role.description,
                'entity_type': role.entity_reference.entity_type if role.entity_reference else None,
                'entity_id': role.entity_reference.entity_id if role.entity_reference else None,
                'is_active': role.is_active,
                'is_system_role': role.is_system_role,
            }
        )
        
        # Sync many-to-many permissions
        permission_ids = [int(p.id) for p in role.permissions]
        orm_role.permissions.set(permission_ids)

    def get_by_id(self, role_id: str) -> Optional[Role]:
        """Retrieves a Role by its UUID."""
        try:
            orm_role = RoleModel.objects.prefetch_related('permissions__content_type').get(id=role_id)
            return RoleMapper.to_domain(orm_role)
        except RoleModel.DoesNotExist:
            return None

    def get_by_name(self, name: str, entity_reference: Optional[EntityReference] = None) -> Optional[Role]:
        """Retrieves a Role by name within a specific scope."""
        entity_type = entity_reference.entity_type if entity_reference else None
        entity_id = entity_reference.entity_id if entity_reference else None
        
        try:
            orm_role = RoleModel.objects.prefetch_related('permissions__content_type').get(
                name=name,
                entity_type=entity_type,
                entity_id=entity_id
            )
            return RoleMapper.to_domain(orm_role)
        except RoleModel.DoesNotExist:
            return None

    def get_all(self) -> List[Role]:
        """Retrieves all Roles from the database."""
        orm_roles = RoleModel.objects.prefetch_related('permissions__content_type').all()
        return [RoleMapper.to_domain(role) for role in orm_roles]

    def get_by_entity(self, entity_type: str, entity_id: str) -> List[Role]:
        """Retrieves all roles scoped to a specific entity."""
        orm_roles = RoleModel.objects.prefetch_related(
            'permissions__content_type'
        ).filter(entity_type=entity_type, entity_id=entity_id)
        return [RoleMapper.to_domain(role) for role in orm_roles]

    def delete(self, role_id: str) -> None:
        """Deletes a Role by its UUID."""
        RoleModel.objects.filter(id=role_id).delete()
