import pytest
from django_permissions_manager.domain.value_objects.user_id import UserId


class TestUserId:
    def test_valid_id_is_accepted(self):
        assert UserId("42").value == "42"

    def test_empty_string_raises(self):
        with pytest.raises(ValueError, match="empty"):
            UserId("")

    def test_whitespace_raises(self):
        with pytest.raises(ValueError, match="empty"):
            UserId("   ")

    def test_numeric_string_is_accepted(self):
        assert UserId("1").value == "1"
