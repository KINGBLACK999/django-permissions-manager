import pytest
from datetime import datetime, timezone
from unittest.mock import MagicMock

from django_permissions_manager.application.use_cases.assign_permission_group_to_role import AssignPermissionGroupToRoleUseCase
from django_permissions_manager.domain.entities.permission import Permission
from django_permissions_manager.domain.entities.permission_group import PermissionGroup
from django_permissions_manager.domain.entities.role import Role
from django_permissions_manager.domain.value_objects.permission_code import PermissionCode
from django_permissions_manager.domain.value_objects.role_name import RoleName


def make_role(permissions=None) -> Role:
    return Role(
        id="role-1", name=RoleName("Editor"), description="", entity_reference=None,
        permissions=permissions or [], is_active=True, is_system_role=False,
        created_at=datetime.now(timezone.utc), updated_at=datetime.now(timezone.utc),
    )


def make_group(codes: list) -> PermissionGroup:
    perms = [
        Permission(id=str(i), code=PermissionCode(c), name=c, content_type="model")
        for i, c in enumerate(codes)
    ]
    return PermissionGroup(id="group-1", name="Content", description="", permissions=perms)


class TestAssignPermissionGroupToRoleUseCase:
    def setup_method(self):
        self.role_repo = MagicMock()
        self.group_repo = MagicMock()
        self.use_case = AssignPermissionGroupToRoleUseCase(
            role_repository=self.role_repo,
            group_repository=self.group_repo,
        )

    def test_merges_group_permissions_into_role(self):
        self.role_repo.get_by_id.return_value = make_role()
        self.group_repo.get_by_id.return_value = make_group(["auth.view_user", "auth.add_user"])

        dto = self.use_case.execute(role_id="role-1", group_id="group-1")

        self.role_repo.save.assert_called_once()
        assert "auth.view_user" in dto.permissions
        assert "auth.add_user" in dto.permissions

    def test_does_not_duplicate_existing_permissions(self):
        existing_perm = Permission(id="0", code=PermissionCode("auth.view_user"), name="view", content_type="model")
        self.role_repo.get_by_id.return_value = make_role(permissions=[existing_perm])
        self.group_repo.get_by_id.return_value = make_group(["auth.view_user"])

        dto = self.use_case.execute(role_id="role-1", group_id="group-1")

        assert dto.permissions.count("auth.view_user") == 1

    def test_raises_when_role_not_found(self):
        self.role_repo.get_by_id.return_value = None
        with pytest.raises(ValueError, match="Role"):
            self.use_case.execute(role_id="bad", group_id="group-1")

    def test_raises_when_group_not_found(self):
        self.role_repo.get_by_id.return_value = make_role()
        self.group_repo.get_by_id.return_value = None
        with pytest.raises(ValueError, match="Permission group"):
            self.use_case.execute(role_id="role-1", group_id="bad")
