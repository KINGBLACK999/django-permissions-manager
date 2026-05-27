import pytest
from datetime import datetime, timezone
from unittest.mock import MagicMock, patch

from django_permissions_manager.domain.entities.role import Role
from django_permissions_manager.domain.exceptions.role_exceptions import (
    RoleAlreadyExistsException,
    SystemRoleDeletionException,
)
from django_permissions_manager.domain.services.role_manager import RoleManager
from django_permissions_manager.domain.value_objects.role_name import RoleName


def make_role(is_system: bool = False, is_active: bool = True) -> Role:
    return Role(
        id="role-1",
        name=RoleName("Editor"),
        description="",
        entity_reference=None,
        permissions=[],
        is_active=is_active,
        is_system_role=is_system,
        created_at=datetime.now(timezone.utc),
        updated_at=datetime.now(timezone.utc),
    )


class TestRoleManager:
    def setup_method(self):
        self.repo = MagicMock()
        self.manager = RoleManager(self.repo)

    def test_deactivate_role_sets_inactive_and_saves(self):
        role = make_role()
        self.manager.deactivate_role(role)
        assert role.is_active is False
        self.repo.save.assert_called_once_with(role)

    def test_deactivate_system_role_raises(self):
        role = make_role(is_system=True)
        with pytest.raises(SystemRoleDeletionException):
            self.manager.deactivate_role(role)
        self.repo.save.assert_not_called()

    def test_activate_role_sets_active_and_saves(self):
        role = make_role(is_active=False)
        self.manager.activate_role(role)
        assert role.is_active is True
        self.repo.save.assert_called_once_with(role)

    def test_ensure_unique_name_raises_if_exists(self):
        existing = make_role()
        self.repo.get_by_name.return_value = existing
        with pytest.raises(RoleAlreadyExistsException):
            self.manager.ensure_role_name_is_unique("Editor")

    def test_ensure_unique_name_passes_if_not_exists(self):
        self.repo.get_by_name.return_value = None
        self.manager.ensure_role_name_is_unique("NewRole")
        self.repo.get_by_name.assert_called_once()
