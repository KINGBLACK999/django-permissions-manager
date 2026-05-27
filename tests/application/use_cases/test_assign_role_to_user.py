import pytest
from datetime import datetime, timezone
from unittest.mock import MagicMock

from django_permissions_manager.application.use_cases.assign_role_to_user import AssignRoleToUserUseCase
from django_permissions_manager.domain.entities.role import Role
from django_permissions_manager.domain.value_objects.role_name import RoleName


def make_role() -> Role:
    return Role(
        id="role-uuid-1",
        name=RoleName("Viewer"),
        description="",
        entity_reference=None,
        permissions=[],
        is_active=True,
        is_system_role=False,
        created_at=datetime.now(timezone.utc),
        updated_at=datetime.now(timezone.utc),
    )


class TestAssignRoleToUserUseCase:
    def setup_method(self):
        self.user_role_repo = MagicMock()
        self.role_repo = MagicMock()
        self.use_case = AssignRoleToUserUseCase(
            user_role_repository=self.user_role_repo,
            role_repository=self.role_repo,
        )

    def test_assigns_role_and_returns_dto(self):
        role = make_role()
        self.role_repo.get_by_id.return_value = role

        dto = self.use_case.execute(user_id="10", role_id="role-uuid-1")

        self.user_role_repo.save.assert_called_once()
        assert dto.user_id == "10"
        assert dto.role_id == "role-uuid-1"
        assert dto.role_name == "Viewer"
        assert dto.assigned_by is None

    def test_assigns_with_assigned_by(self):
        role = make_role()
        self.role_repo.get_by_id.return_value = role

        dto = self.use_case.execute(user_id="10", role_id="role-uuid-1", assigned_by_id="5")

        assert dto.assigned_by == "5"

    def test_raises_when_role_not_found(self):
        self.role_repo.get_by_id.return_value = None

        with pytest.raises(ValueError, match="does not exist"):
            self.use_case.execute(user_id="10", role_id="nonexistent")

        self.user_role_repo.save.assert_not_called()
