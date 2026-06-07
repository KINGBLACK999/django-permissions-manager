import pytest
from django_permissions_manager.domain.value_objects.permission_code import PermissionCode


class TestPermissionCode:
    def test_valid_code_is_accepted(self):
        code = PermissionCode("auth.view_user")
        assert code.value == "auth.view_user"

    def test_missing_dot_raises(self):
        with pytest.raises(ValueError, match="app_label.codename"):
            PermissionCode("authview_user")

    def test_multiple_dots_raises(self):
        with pytest.raises(ValueError, match="app_label.codename"):
            PermissionCode("auth.view.user")

    def test_empty_app_label_raises(self):
        with pytest.raises(ValueError, match="non-empty"):
            PermissionCode(".view_user")

    def test_empty_codename_raises(self):
        with pytest.raises(ValueError, match="non-empty"):
            PermissionCode("auth.")

    def test_equality_is_based_on_value(self):
        assert PermissionCode("auth.view_user") == PermissionCode("auth.view_user")

    def test_different_codes_are_not_equal(self):
        assert PermissionCode("auth.view_user") != PermissionCode("auth.add_user")
