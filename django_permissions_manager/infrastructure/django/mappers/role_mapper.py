from ..models.role_model import RoleModel
from ....domain.entities.role import Role
from ....domain.value_objects.role_name import RoleName
from ....domain.value_objects.entity_reference import EntityReference
from .permission_mapper import PermissionMapper

class RoleMapper:
    """Mapper between RoleModel and Role domain entity."""

    @staticmethod
    def to_domain(orm_model: RoleModel) -> Role:
        """Maps an ORM model to a Domain entity."""
        entity_ref = None
        if orm_model.entity_type and orm_model.entity_id:
            entity_ref = EntityReference(
                entity_type=orm_model.entity_type,
                entity_id=orm_model.entity_id
            )
            
        return Role(
            id=str(orm_model.id),
            name=RoleName(orm_model.name),
            description=orm_model.description,
            entity_reference=entity_ref,
            permissions=[PermissionMapper.to_domain(p) for p in orm_model.permissions.all()],
            is_active=orm_model.is_active,
            is_system_role=orm_model.is_system_role,
            created_at=orm_model.created_at,
            updated_at=orm_model.updated_at
        )

    @staticmethod
    def to_orm(domain_entity: Role) -> RoleModel:
        """Maps a Domain entity to an ORM model (without permissions)."""
        return RoleModel(
            id=domain_entity.id,
            name=domain_entity.name.value,
            description=domain_entity.description,
            entity_type=domain_entity.entity_reference.entity_type if domain_entity.entity_reference else None,
            entity_id=domain_entity.entity_reference.entity_id if domain_entity.entity_reference else None,
            is_active=domain_entity.is_active,
            is_system_role=domain_entity.is_system_role
        )
