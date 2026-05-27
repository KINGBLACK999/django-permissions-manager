"""
Integration tests for DjangoRoleRepository.

These tests hit the real SQLite database (via pytest-django) to verify
that the ORM implementation correctly persists and retrieves domain entities.
"""
import pytest

from django_permissions_manager.infrastructure.django.repositories.django_role_repository import (
    DjangoRoleRepository,
)
from django_permissions_manager.domain.services.role_factory import RoleFactory
from django_permissions_manager.domain.value_objects.entity_reference import EntityReference


@pytest.mark.django_db
class TestDjangoRoleRepositoryIntegration:
    """Integration tests for DjangoRoleRepository against a real database."""

    def setup_method(self):
        self.repo = DjangoRoleRepository()

    # ------------------------------------------------------------------
    # save + get_by_id
    # ------------------------------------------------------------------

    def test_save_and_retrieve_global_role_by_id(self):
        role = RoleFactory.create_role(name="Admin", description="Full access")
        self.repo.save(role)

        retrieved = self.repo.get_by_id(role.id)

        assert retrieved is not None
        assert retrieved.id == role.id
        assert retrieved.name.value == "Admin"
        assert retrieved.description == "Full access"
        assert retrieved.entity_reference is None
        assert retrieved.is_active is True
        assert retrieved.is_system_role is False

    def test_save_and_retrieve_scoped_role_by_id(self):
        entity_ref = EntityReference(entity_type="Company", entity_id="42")
        role = RoleFactory.create_role(
            name="Editor",
            description="Edit access",
            entity_reference=entity_ref,
        )
        self.repo.save(role)

        retrieved = self.repo.get_by_id(role.id)

        assert retrieved is not None
        assert retrieved.entity_reference is not None
        assert retrieved.entity_reference.entity_type == "Company"
        assert retrieved.entity_reference.entity_id == "42"

    def test_get_by_id_returns_none_for_unknown_id(self):
        result = self.repo.get_by_id("00000000-0000-0000-0000-000000000000")
        assert result is None

    # ------------------------------------------------------------------
    # get_by_name
    # ------------------------------------------------------------------

    def test_get_by_name_returns_global_role(self):
        role = RoleFactory.create_role(name="Viewer", description="Read only")
        self.repo.save(role)

        retrieved = self.repo.get_by_name("Viewer")

        assert retrieved is not None
        assert retrieved.name.value == "Viewer"

    def test_get_by_name_with_entity_scope(self):
        entity_ref = EntityReference(entity_type="Project", entity_id="99")
        role = RoleFactory.create_role(
            name="Manager", description="Manage project", entity_reference=entity_ref
        )
        self.repo.save(role)

        retrieved = self.repo.get_by_name("Manager", entity_reference=entity_ref)

        assert retrieved is not None
        assert retrieved.entity_reference.entity_id == "99"

    def test_get_by_name_returns_none_when_not_found(self):
        result = self.repo.get_by_name("NonExistentRole")
        assert result is None

    # ------------------------------------------------------------------
    # get_all
    # ------------------------------------------------------------------

    def test_get_all_returns_saved_roles(self):
        role_a = RoleFactory.create_role(name="RoleA")
        role_b = RoleFactory.create_role(name="RoleB")
        self.repo.save(role_a)
        self.repo.save(role_b)

        all_roles = self.repo.get_all()
        names = [r.name.value for r in all_roles]

        assert "RoleA" in names
        assert "RoleB" in names

    # ------------------------------------------------------------------
    # get_by_entity
    # ------------------------------------------------------------------

    def test_get_by_entity_filters_correctly(self):
        entity_ref = EntityReference(entity_type="Org", entity_id="7")
        role = RoleFactory.create_role(name="OrgAdmin", entity_reference=entity_ref)
        self.repo.save(role)

        # Also save a global role — should NOT appear in results
        self.repo.save(RoleFactory.create_role(name="GlobalRole"))

        scoped = self.repo.get_by_entity("Org", "7")

        assert len(scoped) == 1
        assert scoped[0].name.value == "OrgAdmin"

    # ------------------------------------------------------------------
    # update (save idempotence)
    # ------------------------------------------------------------------

    def test_save_updates_existing_role(self):
        role = RoleFactory.create_role(name="UpdateMe", description="Original")
        self.repo.save(role)

        # Mutate in-memory and save again
        role.description = "Updated"
        role.is_active = False
        self.repo.save(role)

        updated = self.repo.get_by_id(role.id)
        assert updated.description == "Updated"
        assert updated.is_active is False

    # ------------------------------------------------------------------
    # delete
    # ------------------------------------------------------------------

    def test_delete_removes_role(self):
        role = RoleFactory.create_role(name="DeleteMe")
        self.repo.save(role)

        self.repo.delete(role.id)

        assert self.repo.get_by_id(role.id) is None

    def test_delete_nonexistent_role_does_not_raise(self):
        # Should be a no-op
        self.repo.delete("00000000-0000-0000-0000-000000000000")
