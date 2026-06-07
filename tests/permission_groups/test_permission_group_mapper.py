from unittest.mock import MagicMock

from django_permissions_manager.infrastructure.django.mappers.permission_group_mapper import PermissionGroupMapper


def make_permission_orm(id=1, app_label="auth", codename="view_user", model="user", name="Can view user"):
    orm = MagicMock()
    orm.id = id
    orm.content_type.app_label = app_label
    orm.content_type.model = model
    orm.codename = codename
    orm.name = name
    return orm


class TestPermissionGroupMapper:
    def _make_group_orm(self, permissions=None):
        orm = MagicMock()
        orm.id = "group-uuid"
        orm.name = "Content"
        orm.description = "Content permissions"
        orm.permissions.all.return_value = permissions or []
        return orm

    def test_maps_basic_fields(self):
        group = PermissionGroupMapper.to_domain(self._make_group_orm())
        assert group.id == "group-uuid"
        assert group.name == "Content"
        assert group.description == "Content permissions"

    def test_maps_permissions_via_manager(self):
        perm_orm = make_permission_orm(
            app_label="blog", codename="view_post", model="post", name="Can view post"
        )
        group = PermissionGroupMapper.to_domain(self._make_group_orm(permissions=[perm_orm]))
        assert len(group.permissions) == 1
        assert group.permissions[0].code.value == "blog.view_post"

    def test_empty_permissions_list(self):
        group = PermissionGroupMapper.to_domain(self._make_group_orm())
        assert group.permissions == []
