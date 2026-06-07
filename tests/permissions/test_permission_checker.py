import pytest
from datetime import datetime, timezone
from unittest.mock import MagicMock

from django_permissions_manager.domain.entities.permission import Permission
from django_permissions_manager.domain.entities.role import Role
from django_permissions_manager.domain.entities.user_role import UserRole
from django_permissions_manager.domain.services.permission_checker import PermissionChecker
from django_permissions_manager.domain.value_objects.permission_code import PermissionCode
from django_permissions_manager.domain.value_objects.role_name import RoleName
from django_permissions_manager.domain.value_objects.user_id import UserId


def make_permission(code: str) -> Permission:
    return Permission(id="1", code=PermissionCode(code), name=code, content_type="model")


def make_role(permissions: list, is_active: bool = True) -> Role:
    return Role(
        id="role-1",
        name=RoleName("Test Role"),
        description="",
        entity_reference=None,
        permissions=permissions,
        is_active=is_active,
        is_system_role=False,
        created_at=datetime.now(timezone.utc),
        updated_at=datetime.now(timezone.utc),
    )


def make_user_role(role: Role) -> UserRole:
    return UserRole(
        id="ur-1",
        user_id=UserId("42"),
        role=role,
        assigned_at=datetime.now(timezone.utc),
        assigned_by=None,
    )


class TestPermissionChecker:
    def test_returns_true_when_role_has_permission(self):
        perm = make_permission("auth.view_user")
        role = make_role([perm])
        user_roles = [make_user_role(role)]
        assert PermissionChecker.has_permission(user_roles, "auth.view_user") is True

    def test_returns_false_when_role_lacks_permission(self):
        perm = make_permission("auth.add_user")
        role = make_role([perm])
        user_roles = [make_user_role(role)]
        assert PermissionChecker.has_permission(user_roles, "auth.view_user") is False

    def test_returns_false_when_role_is_inactive(self):
        perm = make_permission("auth.view_user")
        role = make_role([perm], is_active=False)
        user_roles = [make_user_role(role)]
        assert PermissionChecker.has_permission(user_roles, "auth.view_user") is False

    def test_returns_false_with_no_roles(self):
        assert PermissionChecker.has_permission([], "auth.view_user") is False

    def test_has_any_permission_returns_true_on_partial_match(self):
        perm = make_permission("auth.view_user")
        role = make_role([perm])
        user_roles = [make_user_role(role)]
        result = PermissionChecker.has_any_permission(
            user_roles, ["auth.view_user", "auth.add_user"]
        )
        assert result is True

    def test_has_any_permission_returns_false_with_no_match(self):
        role = make_role([])
        user_roles = [make_user_role(role)]
        assert PermissionChecker.has_any_permission(user_roles, ["auth.view_user"]) is False

    def test_has_all_permissions_returns_true_when_all_present(self):
        perms = [make_permission("auth.view_user"), make_permission("auth.add_user")]
        role = make_role(perms)
        user_roles = [make_user_role(role)]
        assert PermissionChecker.has_all_permissions(
            user_roles, ["auth.view_user", "auth.add_user"]
        ) is True

    def test_has_all_permissions_returns_false_when_one_missing(self):
        perm = make_permission("auth.view_user")
        role = make_role([perm])
        user_roles = [make_user_role(role)]
        assert PermissionChecker.has_all_permissions(
            user_roles, ["auth.view_user", "auth.add_user"]
        ) is False
