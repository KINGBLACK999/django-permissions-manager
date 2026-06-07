from unittest.mock import MagicMock

from django_permissions_manager.infrastructure.django.mappers.permission_mapper import PermissionMapper


def make_permission_orm(id=1, app_label="auth", codename="view_user", model="user", name="Can view user"):
    orm = MagicMock()
    orm.id = id
    orm.content_type.app_label = app_label
    orm.content_type.model = model
    orm.codename = codename
    orm.name = name
    return orm


class TestPermissionMapper:
    def test_builds_code_from_app_label_and_codename(self):
        orm = make_permission_orm(app_label="auth", codename="view_user")
        perm = PermissionMapper.to_domain(orm)
        assert perm.code.value == "auth.view_user"

    def test_casts_id_to_string(self):
        orm = make_permission_orm(id=42)
        perm = PermissionMapper.to_domain(orm)
        assert perm.id == "42"

    def test_maps_name_and_content_type_model(self):
        orm = make_permission_orm(model="user", name="Can view user")
        perm = PermissionMapper.to_domain(orm)
        assert perm.name == "Can view user"
        assert perm.content_type == "user"
