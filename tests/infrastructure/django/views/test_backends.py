import pytest
from unittest.mock import MagicMock, patch

from django_permissions_manager.infrastructure.django.views.backends import (
    PermissionsManagerBackend,
    _CACHE_ATTR,
)


def make_user(is_active=True, is_superuser=False):
    user = MagicMock()
    user.is_active = is_active
    user.is_superuser = is_superuser
    user.id = 1
    if hasattr(user, _CACHE_ATTR):
        delattr(user, _CACHE_ATTR)
    return user


class TestPermissionsManagerBackend:
    def setup_method(self):
        self.backend = PermissionsManagerBackend()

    def test_inactive_user_is_denied(self):
        user = make_user(is_active=False)
        assert self.backend.has_perm(user, "auth.view_user") is False

    def test_superuser_is_always_allowed(self):
        user = make_user(is_superuser=True)
        assert self.backend.has_perm(user, "auth.view_user") is True

    def test_delegates_to_use_case_for_regular_user(self):
        user = make_user()
        mock_use_case = MagicMock()
        mock_use_case.execute.return_value = True

        with patch(
            "django_permissions_manager.infrastructure.django.views.backends.get_check_permission_use_case",
            return_value=mock_use_case,
        ):
            result = self.backend.has_perm(user, "auth.view_user")

        assert result is True
        mock_use_case.execute.assert_called_once_with(
            user_id="1", permission_code="auth.view_user"
        )

    def test_caches_result_on_second_call(self):
        user = make_user()
        mock_use_case = MagicMock()
        mock_use_case.execute.return_value = True

        with patch(
            "django_permissions_manager.infrastructure.django.views.backends.get_check_permission_use_case",
            return_value=mock_use_case,
        ):
            self.backend.has_perm(user, "auth.view_user")
            self.backend.has_perm(user, "auth.view_user")

        # Use case should only be called once — second call hits cache
        mock_use_case.execute.assert_called_once()

    def test_different_permissions_are_cached_independently(self):
        user = make_user()
        mock_use_case = MagicMock()
        mock_use_case.execute.side_effect = [True, False]

        with patch(
            "django_permissions_manager.infrastructure.django.views.backends.get_check_permission_use_case",
            return_value=mock_use_case,
        ):
            r1 = self.backend.has_perm(user, "auth.view_user")
            r2 = self.backend.has_perm(user, "auth.add_user")

        assert r1 is True
        assert r2 is False
        assert mock_use_case.execute.call_count == 2

    def test_get_user_returns_none(self):
        assert self.backend.get_user(1) is None
