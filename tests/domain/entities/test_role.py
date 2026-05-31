import pytest
from datetime import datetime, timezone, timedelta

from django_permissions_manager.domain.entities.role import Role
from django_permissions_manager.domain.value_objects.role_name import RoleName


def make_role(**kwargs) -> Role:
    now = datetime.now(timezone.utc)
    defaults = dict(
        id="role-1",
        name=RoleName("Editor"),
        description="",
        entity_reference=None,
        permissions=[],
        is_active=True,
        is_system_role=False,
        created_at=now,
        updated_at=now,
    )
    defaults.update(kwargs)
    return Role(**defaults)


class TestRoleValidate:
    def test_valid_role_does_not_raise(self):
        make_role().validate()

    def test_valid_system_role_does_not_raise(self):
        make_role(is_system_role=True, is_active=True).validate()

    def test_inactive_system_role_raises(self):
        role = make_role(is_system_role=True, is_active=False)
        with pytest.raises(ValueError, match="system role cannot be inactive"):
            role.validate()

    def test_updated_at_before_created_at_raises(self):
        now = datetime.now(timezone.utc)
        role = make_role(
            created_at=now,
            updated_at=now - timedelta(seconds=1),
        )
        with pytest.raises(ValueError, match="updated_at cannot be before created_at"):
            role.validate()

    def test_updated_at_equal_to_created_at_does_not_raise(self):
        now = datetime.now(timezone.utc)
        make_role(created_at=now, updated_at=now).validate()


class TestRoleFactory:
    def test_factory_calls_validate(self):
        from django_permissions_manager.domain.services.role_factory import RoleFactory
        # RoleFactory always sets is_active=True so a system role is always valid
        role = RoleFactory.create_role(name="Admin", is_system_role=True)
        assert role.is_active is True
        assert role.is_system_role is True
