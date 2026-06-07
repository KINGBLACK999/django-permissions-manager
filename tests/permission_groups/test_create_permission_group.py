import pytest
from unittest.mock import MagicMock

from django_permissions_manager.application.use_cases.create_permission_group import CreatePermissionGroupUseCase


class TestCreatePermissionGroupUseCase:
    def setup_method(self):
        self.group_repo = MagicMock()
        self.perm_repo = MagicMock()
        self.use_case = CreatePermissionGroupUseCase(
            group_repository=self.group_repo,
            permission_repository=self.perm_repo,
        )

    def test_creates_group_and_returns_dto(self):
        self.group_repo.get_by_name.return_value = None
        self.perm_repo.get_by_code.return_value = None

        dto = self.use_case.execute(name="Content Editors", description="Edit permissions")

        self.group_repo.save.assert_called_once()
        assert dto.name == "Content Editors"
        assert dto.permissions == []

    def test_raises_when_group_name_already_exists(self):
        self.group_repo.get_by_name.return_value = MagicMock()

        with pytest.raises(ValueError, match="already exists"):
            self.use_case.execute(name="Content Editors")

        self.group_repo.save.assert_not_called()

    def test_resolves_permission_codes(self):
        from django_permissions_manager.domain.entities.permission import Permission
        from django_permissions_manager.domain.value_objects.permission_code import PermissionCode

        self.group_repo.get_by_name.return_value = None
        perm = Permission(id="1", code=PermissionCode("auth.view_user"), name="view user", content_type="user")
        self.perm_repo.get_by_code.return_value = perm

        dto = self.use_case.execute(name="Viewers", permission_codes=["auth.view_user"])

        assert "auth.view_user" in dto.permissions
