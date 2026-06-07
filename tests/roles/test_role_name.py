import pytest
from django_permissions_manager.domain.value_objects.role_name import RoleName, MAX_ROLE_NAME_LENGTH


class TestRoleName:
    def test_valid_name_is_accepted(self):
        assert RoleName("Admin").value == "Admin"

    def test_empty_string_raises(self):
        with pytest.raises(ValueError, match="empty"):
            RoleName("")

    def test_whitespace_only_raises(self):
        with pytest.raises(ValueError, match="empty"):
            RoleName("   ")

    def test_name_exceeding_max_length_raises(self):
        with pytest.raises(ValueError, match="255"):
            RoleName("x" * (MAX_ROLE_NAME_LENGTH + 1))

    def test_name_at_max_length_is_accepted(self):
        name = RoleName("x" * MAX_ROLE_NAME_LENGTH)
        assert len(name.value) == MAX_ROLE_NAME_LENGTH
