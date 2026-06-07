import pytest
from datetime import datetime, timezone
from unittest.mock import MagicMock

from django_permissions_manager.application.use_cases.check_user_permission import CheckUserPermissionUseCase
from django_permissions_manager.domain.entities.permission import Permission
from django_permissions_manager.domain.entities.role import Role
from django_permissions_manager.domain.entities.user_role import UserRole
from django_permissions_manager.domain.services.permission_checker import PermissionChecker
from django_permissions_manager.domain.value_objects.permission_code import PermissionCode
from django_permissions_manager.domain.value_objects.role_name import RoleName
from django_permissions_manager.domain.value_objects.user_id import UserId


def _build_user_role_with_perm(code: str) -> UserRole:
    perm = Permission(id="1", code=PermissionCode(code), name=code, content_type="model")
    role = Role(
        id="r1", name=RoleName("Admin"), description="", entity_reference=None,
        permissions=[perm], is_active=True, is_system_role=False,
        created_at=datetime.now(timezone.utc), updated_at=datetime.now(timezone.utc),
    )
    return UserRole(id="ur1", user_id=UserId("1"), role=role,
                    assigned_at=datetime.now(timezone.utc), assigned_by=None)


class TestCheckUserPermissionUseCase:
    def setup_method(self):
        self.user_role_repo = MagicMock()
        self.use_case = CheckUserPermissionUseCase(
            user_role_repository=self.user_role_repo,
            permission_checker=PermissionChecker(),
        )

    def test_returns_true_when_user_has_permission(self):
        self.user_role_repo.get_by_user_id.return_value = [
            _build_user_role_with_perm("auth.view_user")
        ]
        assert self.use_case.execute("1", "auth.view_user") is True

    def test_returns_false_when_user_lacks_permission(self):
        self.user_role_repo.get_by_user_id.return_value = [
            _build_user_role_with_perm("auth.add_user")
        ]
        assert self.use_case.execute("1", "auth.view_user") is False

    def test_returns_false_when_user_has_no_roles(self):
        self.user_role_repo.get_by_user_id.return_value = []
        assert self.use_case.execute("1", "auth.view_user") is False

    def test_passes_correct_user_id_to_repository(self):
        self.user_role_repo.get_by_user_id.return_value = []
        self.use_case.execute("99", "auth.view_user")
        self.user_role_repo.get_by_user_id.assert_called_once_with(UserId("99"))
