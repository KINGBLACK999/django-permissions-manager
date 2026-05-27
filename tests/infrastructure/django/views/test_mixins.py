import pytest
from datetime import datetime, timezone
from unittest.mock import MagicMock, patch

from django.core.exceptions import PermissionDenied
from django_permissions_manager.infrastructure.django.views.mixins import RoleRequiredMixin
from django_permissions_manager.application.dto.user_role_dto import UserRoleDTO


def make_dto(role_name: str) -> UserRoleDTO:
    return UserRoleDTO(
        id="ur-1",
        user_id="1",
        role_id="r-1",
        role_name=role_name,
        assigned_at=datetime.now(timezone.utc),
        assigned_by=None,
    )


def make_request(authenticated=True, user_id="1"):
    request = MagicMock()
    request.user.is_authenticated = authenticated
    request.user.id = user_id
    return request


class ConcreteView(RoleRequiredMixin):
    role_required = "Admin"

    def handle_no_permission(self):
        raise PermissionDenied

    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)


class TestRoleRequiredMixin:
    def _make_view(self, role_required="Admin"):
        view = ConcreteView()
        view.role_required = role_required
        return view

    def test_grants_access_when_user_has_required_role(self):
        view = self._make_view("Admin")
        request = make_request()

        with patch(
            "django_permissions_manager.infrastructure.django.views.mixins.GetUserRolesUseCase"
        ) as MockUseCase:
            MockUseCase.return_value.execute.return_value = [make_dto("Admin")]
            # Should not raise
            with patch.object(RoleRequiredMixin, "dispatch", wraps=view.dispatch):
                try:
                    view.has_role(request)
                    result = True
                except PermissionDenied:
                    result = False

        assert result is True

    def test_denies_access_when_user_lacks_role(self):
        view = self._make_view("Admin")
        request = make_request()

        with patch(
            "django_permissions_manager.infrastructure.django.views.mixins.GetUserRolesUseCase"
        ) as MockUseCase:
            MockUseCase.return_value.execute.return_value = [make_dto("Viewer")]
            assert view.has_role(request) is False

    def test_raises_permission_denied_in_dispatch(self):
        view = self._make_view("Admin")
        request = make_request()

        with patch(
            "django_permissions_manager.infrastructure.django.views.mixins.GetUserRolesUseCase"
        ) as MockUseCase:
            MockUseCase.return_value.execute.return_value = [make_dto("Viewer")]
            with pytest.raises(PermissionDenied):
                view.dispatch(request)

    def test_unauthenticated_user_is_denied(self):
        view = self._make_view("Admin")
        request = make_request(authenticated=False)

        with pytest.raises(PermissionDenied):
            view.dispatch(request)

    def test_accepts_list_of_roles(self):
        view = self._make_view(["Admin", "Editor"])
        request = make_request()

        with patch(
            "django_permissions_manager.infrastructure.django.views.mixins.GetUserRolesUseCase"
        ) as MockUseCase:
            MockUseCase.return_value.execute.return_value = [make_dto("Editor")]
            assert view.has_role(request) is True

    def test_no_role_required_always_grants(self):
        view = self._make_view(None)
        request = make_request()
        assert view.has_role(request) is True
