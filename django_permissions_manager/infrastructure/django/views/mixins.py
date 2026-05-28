from django.contrib.auth.mixins import AccessMixin, PermissionRequiredMixin
from django.core.exceptions import PermissionDenied
from ..services import get_user_roles_use_case


class PermissionManagerMixin(PermissionRequiredMixin):
    """
    Mixin for Django views that requires a specific permission.
    Works seamlessly with PermissionsManagerBackend.
    """
    pass


class RoleRequiredMixin(AccessMixin):
    """
    Mixin to restrict view access to users that have a specific role by name.

    Set `role_required` to a role name string or a list of role name strings.
    The user must have at least one of the listed roles to access the view.
    """
    role_required = None

    def _get_required_roles(self):
        if isinstance(self.role_required, str):
            return {self.role_required}
        return set(self.role_required or [])

    def has_role(self, request):
        required = self._get_required_roles()
        if not required:
            return True

        use_case = get_user_roles_use_case()
        user_roles = use_case.execute(user_id=str(request.user.id))
        assigned_role_names = {ur.role_name for ur in user_roles}
        return bool(required & assigned_role_names)

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return self.handle_no_permission()

        if not self.has_role(request):
            raise PermissionDenied

        return super().dispatch(request, *args, **kwargs)
