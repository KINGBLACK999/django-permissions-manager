"""
Integration tests for DjangoUserRoleRepository.

These tests hit the real SQLite database (via pytest-django) to verify
that user-role assignments are correctly persisted and retrieved.
"""
import uuid
from datetime import datetime, timezone

import pytest
from django.contrib.auth import get_user_model

from django_permissions_manager.infrastructure.django.repositories.django_role_repository import (
    DjangoRoleRepository,
)
from django_permissions_manager.infrastructure.django.repositories.django_user_role_repository import (
    DjangoUserRoleRepository,
)
from django_permissions_manager.domain.entities.user_role import UserRole
from django_permissions_manager.domain.services.role_factory import RoleFactory
from django_permissions_manager.domain.value_objects.user_id import UserId

User = get_user_model()


@pytest.fixture
def role_repo():
    return DjangoRoleRepository()


@pytest.fixture
def user_role_repo():
    return DjangoUserRoleRepository()


@pytest.fixture
def saved_role(role_repo):
    """Persists a Role and returns the domain entity."""
    role = RoleFactory.create_role(name="Tester", description="Test role")
    role_repo.save(role)
    return role


@pytest.fixture
def django_user(db):
    """Creates a real Django user for FK constraints."""
    return User.objects.create_user(username="testuser", password="secret")


@pytest.fixture
def django_assigner(db):
    """Creates a second Django user to represent the assigner."""
    return User.objects.create_user(username="assigner", password="secret")


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _make_user_role(user, role, assigner=None) -> UserRole:
    return UserRole(
        id=str(uuid.uuid4()),
        user_id=UserId(str(user.id)),
        role=role,
        assigned_at=datetime.now(timezone.utc),
        assigned_by=UserId(str(assigner.id)) if assigner else None,
    )


# ---------------------------------------------------------------------------
# Tests
# ---------------------------------------------------------------------------

@pytest.mark.django_db
class TestDjangoUserRoleRepositoryIntegration:

    def test_save_and_retrieve_by_id(
        self, user_role_repo, saved_role, django_user
    ):
        user_role = _make_user_role(django_user, saved_role)
        user_role_repo.save(user_role)

        retrieved = user_role_repo.get_by_id(user_role.id)

        assert retrieved is not None
        assert retrieved.id == user_role.id
        assert retrieved.user_id.value == str(django_user.id)
        assert retrieved.role.name.value == "Tester"

    def test_get_by_id_returns_none_for_unknown(self, user_role_repo):
        result = user_role_repo.get_by_id("00000000-0000-0000-0000-000000000000")
        assert result is None

    def test_save_with_assigned_by(
        self, user_role_repo, saved_role, django_user, django_assigner
    ):
        user_role = _make_user_role(django_user, saved_role, assigner=django_assigner)
        user_role_repo.save(user_role)

        retrieved = user_role_repo.get_by_id(user_role.id)

        assert retrieved.assigned_by is not None
        assert retrieved.assigned_by.value == str(django_assigner.id)

    def test_get_by_user_id_returns_all_assignments(
        self, role_repo, user_role_repo, django_user
    ):
        role_a = RoleFactory.create_role(name="RoleX")
        role_b = RoleFactory.create_role(name="RoleY")
        role_repo.save(role_a)
        role_repo.save(role_b)

        ur_a = _make_user_role(django_user, role_a)
        ur_b = _make_user_role(django_user, role_b)
        user_role_repo.save(ur_a)
        user_role_repo.save(ur_b)

        assignments = user_role_repo.get_by_user_id(UserId(str(django_user.id)))
        role_names = [a.role.name.value for a in assignments]

        assert "RoleX" in role_names
        assert "RoleY" in role_names

    def test_get_by_user_id_returns_empty_for_unknown_user(self, user_role_repo):
        result = user_role_repo.get_by_user_id(UserId("999999"))
        assert result == []

    def test_get_by_role_id_returns_all_users_with_role(
        self, role_repo, user_role_repo, django_user, django_assigner, saved_role
    ):
        ur_a = _make_user_role(django_user, saved_role)
        ur_b = _make_user_role(django_assigner, saved_role)
        user_role_repo.save(ur_a)
        user_role_repo.save(ur_b)

        assignments = user_role_repo.get_by_role_id(saved_role.id)
        user_ids = [a.user_id.value for a in assignments]

        assert str(django_user.id) in user_ids
        assert str(django_assigner.id) in user_ids

    def test_delete_removes_assignment(
        self, user_role_repo, saved_role, django_user
    ):
        user_role = _make_user_role(django_user, saved_role)
        user_role_repo.save(user_role)

        user_role_repo.delete(user_role.id)

        assert user_role_repo.get_by_id(user_role.id) is None

    def test_delete_nonexistent_assignment_does_not_raise(self, user_role_repo):
        user_role_repo.delete("00000000-0000-0000-0000-000000000000")
