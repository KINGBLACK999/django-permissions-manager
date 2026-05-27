import pytest
from unittest.mock import MagicMock, patch

from django_permissions_manager.infrastructure.django.views.backends import (
    PermissionsManagerBackend,
    _CACHE_ATTR,
)


class FakeUser:
    """Plain object so hasattr/setattr behave correctly for cache tests."""
    is_active = True
    is_superuser = False
    id = 1


def make_user():
    return FakeUser()


class TestBackendCacheSettings:
    def setup_method(self):
        self.backend = PermissionsManagerBackend()

    def test_bypasses_cache_when_cache_disabled(self):
        user = make_user()
        mock_use_case = MagicMock()
        mock_use_case.execute.return_value = True

        with patch(
            "django_permissions_manager.infrastructure.django.views.backends.get_check_permission_use_case",
            return_value=mock_use_case,
        ), patch(
            "django_permissions_manager.infrastructure.django.views.backends.app_settings"
        ) as mock_settings:
            mock_settings.CACHE_ENABLED = False
            self.backend.has_perm(user, "auth.view_user")
            self.backend.has_perm(user, "auth.view_user")

        # Without cache, use case must be called twice
        assert mock_use_case.execute.call_count == 2

    def test_uses_cache_when_cache_enabled(self):
        user = make_user()
        mock_use_case = MagicMock()
        mock_use_case.execute.return_value = True

        with patch(
            "django_permissions_manager.infrastructure.django.views.backends.get_check_permission_use_case",
            return_value=mock_use_case,
        ), patch(
            "django_permissions_manager.infrastructure.django.views.backends.app_settings"
        ) as mock_settings:
            mock_settings.CACHE_ENABLED = True
            self.backend.has_perm(user, "auth.view_user")
            self.backend.has_perm(user, "auth.view_user")

        # With cache, use case must be called only once
        assert mock_use_case.execute.call_count == 1
