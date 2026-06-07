import pytest
from datetime import datetime, timezone
from unittest.mock import MagicMock

from django_permissions_manager.application.use_cases.update_role_permissions import UpdateRolePermissionsUseCase
from django_permissions_manager.domain.entities.permission import Permission
from django_permissions_manager.domain.entities.role import Role
from django_permissions_manager.domain.value_objects.permission_code import PermissionCode
from django_permissions_manager.domain.value_objects.role_name import RoleName


def make_role(permissions=None) -> Role:
    return Role(
        id="role-1",
        name=RoleName("Editor"),
        description="Edit content",
        entity_reference=None,
        permissions=permissions or [],
        is_active=True,
        is_system_role=False,
        created_at=datetime.now(timezone.utc),
        updated_at=datetime.now(timezone.utc),
    )


def make_permission(id: str, code: str) -> Permission:
    return Permission(id=id, code=PermissionCode(code), name=code, content_type="model")


class TestUpdateRolePermissionsUseCase:
    def setup_method(self):
        self.role_repo = MagicMock()
        self.perm_repo = MagicMock()
        self.use_case = UpdateRolePermissionsUseCase(
            role_repository=self.role_repo,
            permission_repository=self.perm_repo,
        )

    def test_replaces_permissions_and_returns_dto(self):
        self.role_repo.get_by_id.return_value = make_role()
        perm = make_permission("p1", "auth.view_user")
        self.perm_repo.get_by_code.return_value = perm

        dto = self.use_case.execute(role_id="role-1", permission_codes=["auth.view_user"])

        self.role_repo.save.assert_called_once()
        assert dto.id == "role-1"
        assert dto.permissions == ["auth.view_user"]

    def test_replaces_not_merges_existing_permissions(self):
        existing = make_permission("old", "auth.delete_user")
        self.role_repo.get_by_id.return_value = make_role(permissions=[existing])
        new_perm = make_permission("p1", "auth.view_user")
        self.perm_repo.get_by_code.return_value = new_perm

        dto = self.use_case.execute(role_id="role-1", permission_codes=["auth.view_user"])

        assert "auth.view_user" in dto.permissions
        assert "auth.delete_user" not in dto.permissions

    def test_empty_codes_clears_all_permissions(self):
        existing = make_permission("p1", "auth.view_user")
        self.role_repo.get_by_id.return_value = make_role(permissions=[existing])

        dto = self.use_case.execute(role_id="role-1", permission_codes=[])

        self.role_repo.save.assert_called_once()
        assert dto.permissions == []

    def test_silently_skips_unknown_permission_codes(self):
        self.role_repo.get_by_id.return_value = make_role()
        known = make_permission("p1", "auth.view_user")
        self.perm_repo.get_by_code.side_effect = lambda code: (
            known if code.value == "auth.view_user" else None
        )

        dto = self.use_case.execute(
            role_id="role-1",
            permission_codes=["auth.view_user", "nonexistent.perm"],
        )

        assert dto.permissions == ["auth.view_user"]

    def test_raises_when_role_not_found(self):
        self.role_repo.get_by_id.return_value = None

        with pytest.raises(ValueError, match="role-999"):
            self.use_case.execute(role_id="role-999", permission_codes=[])

        self.role_repo.save.assert_not_called()

    def test_resolves_multiple_permissions(self):
        self.role_repo.get_by_id.return_value = make_role()
        perms = {
            "auth.view_user": make_permission("p1", "auth.view_user"),
            "auth.add_user": make_permission("p2", "auth.add_user"),
        }
        self.perm_repo.get_by_code.side_effect = lambda code: perms.get(code.value)

        dto = self.use_case.execute(
            role_id="role-1",
            permission_codes=["auth.view_user", "auth.add_user"],
        )

        assert set(dto.permissions) == {"auth.view_user", "auth.add_user"}
        assert self.role_repo.save.call_count == 1

    def test_dto_preserves_role_metadata(self):
        self.role_repo.get_by_id.return_value = make_role()
        self.perm_repo.get_by_code.return_value = None

        dto = self.use_case.execute(role_id="role-1", permission_codes=[])

        assert dto.name == "Editor"
        assert dto.description == "Edit content"
        assert dto.entity_type is None
        assert dto.entity_id is None
        assert dto.is_active is True
        assert dto.is_system_role is False
