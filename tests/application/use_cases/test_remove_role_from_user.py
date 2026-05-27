import pytest
from datetime import datetime, timezone
from unittest.mock import MagicMock

from django_permissions_manager.application.use_cases.remove_role_from_user import RemoveRoleFromUserUseCase
from django_permissions_manager.domain.entities.role import Role
from django_permissions_manager.domain.entities.user_role import UserRole
from django_permissions_manager.domain.value_objects.role_name import RoleName
from django_permissions_manager.domain.value_objects.user_id import UserId


def make_user_role() -> UserRole:
    role = Role(
        id="role-1", name=RoleName("Admin"), description="", entity_reference=None,
        permissions=[], is_active=True, is_system_role=False,
        created_at=datetime.now(timezone.utc), updated_at=datetime.now(timezone.utc),
    )
    return UserRole(
        id="ur-1", user_id=UserId("10"), role=role,
        assigned_at=datetime.now(timezone.utc), assigned_by=None,
    )


class TestRemoveRoleFromUserUseCase:
    def setup_method(self):
        self.repo = MagicMock()
        self.use_case = RemoveRoleFromUserUseCase(user_role_repository=self.repo)

    def test_removes_existing_assignment(self):
        self.repo.get_by_id.return_value = make_user_role()
        self.use_case.execute("ur-1")
        self.repo.delete.assert_called_once_with("ur-1")

    def test_raises_when_assignment_not_found(self):
        self.repo.get_by_id.return_value = None
        with pytest.raises(ValueError, match="does not exist"):
            self.use_case.execute("nonexistent")
        self.repo.delete.assert_not_called()

    def test_emits_role_revoked_signal(self):
        from django_permissions_manager.infrastructure.django.signals import role_revoked
        self.repo.get_by_id.return_value = make_user_role()

        received = []

        def handler(sender, **kw):
            received.append(kw)

        role_revoked.connect(handler, weak=False)
        try:
            self.use_case.execute("ur-1")
        finally:
            role_revoked.disconnect(handler)

        assert len(received) == 1
        assert received[0]['user_id'] == "10"
        assert received[0]['role_id'] == "role-1"
