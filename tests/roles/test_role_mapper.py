from datetime import datetime, timezone
from unittest.mock import MagicMock

from django_permissions_manager.infrastructure.django.mappers.role_mapper import RoleMapper
from django_permissions_manager.domain.entities.role import Role
from django_permissions_manager.domain.value_objects.entity_reference import EntityReference
from django_permissions_manager.domain.value_objects.role_name import RoleName


def make_permission_orm(id=1, app_label="auth", codename="view_user", model="user", name="Can view user"):
    orm = MagicMock()
    orm.id = id
    orm.content_type.app_label = app_label
    orm.content_type.model = model
    orm.codename = codename
    orm.name = name
    return orm


def make_role_orm(entity_type=None, entity_id=None, permissions=None):
    orm = MagicMock()
    orm.id = "role-uuid"
    orm.name = "Editor"
    orm.description = "Edit content"
    orm.entity_type = entity_type
    orm.entity_id = entity_id
    orm.permissions.all.return_value = permissions or []
    orm.is_active = True
    orm.is_system_role = False
    orm.created_at = datetime.now(timezone.utc)
    orm.updated_at = datetime.now(timezone.utc)
    return orm


def make_role_domain(entity_reference=None):
    return Role(
        id="role-1",
        name=RoleName("Editor"),
        description="Edit content",
        entity_reference=entity_reference,
        permissions=[],
        is_active=True,
        is_system_role=False,
        created_at=datetime.now(timezone.utc),
        updated_at=datetime.now(timezone.utc),
    )


class TestRoleMapper:
    def test_to_domain_global_role_has_no_entity_reference(self):
        role = RoleMapper.to_domain(make_role_orm())
        assert role.entity_reference is None

    def test_to_domain_scoped_role_sets_entity_reference(self):
        role = RoleMapper.to_domain(make_role_orm(entity_type="Company", entity_id="1"))
        assert role.entity_reference.entity_type == "Company"
        assert role.entity_reference.entity_id == "1"

    def test_to_domain_maps_scalar_fields(self):
        role = RoleMapper.to_domain(make_role_orm())
        assert role.id == "role-uuid"
        assert role.name.value == "Editor"
        assert role.description == "Edit content"
        assert role.is_active is True
        assert role.is_system_role is False

    def test_to_domain_maps_permissions_via_manager(self):
        perm_orm = make_permission_orm()
        role = RoleMapper.to_domain(make_role_orm(permissions=[perm_orm]))
        assert len(role.permissions) == 1
        assert role.permissions[0].code.value == "auth.view_user"

    def test_to_domain_empty_permissions_list(self):
        role = RoleMapper.to_domain(make_role_orm(permissions=[]))
        assert role.permissions == []

    def test_to_orm_maps_scalar_fields(self):
        orm = RoleMapper.to_orm(make_role_domain())
        assert orm.name == "Editor"
        assert orm.description == "Edit content"
        assert orm.is_active is True
        assert orm.is_system_role is False

    def test_to_orm_global_role_has_null_entity_fields(self):
        orm = RoleMapper.to_orm(make_role_domain())
        assert orm.entity_type is None
        assert orm.entity_id is None

    def test_to_orm_scoped_role_maps_entity_fields(self):
        domain = make_role_domain(entity_reference=EntityReference("Company", "1"))
        orm = RoleMapper.to_orm(domain)
        assert orm.entity_type == "Company"
        assert orm.entity_id == "1"
