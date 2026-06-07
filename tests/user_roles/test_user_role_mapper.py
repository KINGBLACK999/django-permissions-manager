from datetime import datetime, timezone
from unittest.mock import MagicMock

from django_permissions_manager.infrastructure.django.mappers.user_role_mapper import UserRoleMapper


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


class TestUserRoleMapper:
    def _make_user_role_orm(self, assigned_by_id=None):
        orm = MagicMock()
        orm.id = "ur-uuid"
        orm.user_id = "user-1"
        orm.role = make_role_orm()
        orm.assigned_at = datetime.now(timezone.utc)
        orm.assigned_by_id = assigned_by_id
        return orm

    def test_maps_id_and_user_id(self):
        user_role = UserRoleMapper.to_domain(self._make_user_role_orm())
        assert user_role.id == "ur-uuid"
        assert user_role.user_id.value == "user-1"

    def test_maps_assigned_by_when_present(self):
        user_role = UserRoleMapper.to_domain(self._make_user_role_orm(assigned_by_id="admin-1"))
        assert user_role.assigned_by is not None
        assert user_role.assigned_by.value == "admin-1"

    def test_assigned_by_is_none_when_absent(self):
        user_role = UserRoleMapper.to_domain(self._make_user_role_orm(assigned_by_id=None))
        assert user_role.assigned_by is None

    def test_delegates_role_mapping_to_role_mapper(self):
        user_role = UserRoleMapper.to_domain(self._make_user_role_orm())
        assert user_role.role.name.value == "Editor"
        assert user_role.role.entity_reference is None
