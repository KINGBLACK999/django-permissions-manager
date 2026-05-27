from django.contrib.auth.backends import BaseBackend
from ..services import get_check_permission_use_case
from ..settings import app_settings

_CACHE_ATTR = '_pm_perm_cache'


class PermissionsManagerBackend(BaseBackend):
    """
    Custom Django Authentication Backend.
    Integrates our hexagonal permission logic into Django's user.has_perm().
    """

    def has_perm(self, user_obj, perm, obj=None):
        """
        Check if the user has a specific permission.
        perm: string in 'app_label.codename' format.
        """
        if not user_obj.is_active:
            return False

        if user_obj.is_superuser:
            return True

        if app_settings.CACHE_ENABLED:
            if not hasattr(user_obj, _CACHE_ATTR):
                setattr(user_obj, _CACHE_ATTR, {})
            cache = getattr(user_obj, _CACHE_ATTR)
            if perm not in cache:
                use_case = get_check_permission_use_case()
                cache[perm] = use_case.execute(user_id=str(user_obj.id), permission_code=perm)
            return cache[perm]

        use_case = get_check_permission_use_case()
        return use_case.execute(user_id=str(user_obj.id), permission_code=perm)

    def get_user(self, user_id):
        # We don't handle authentication (login), just authorization
        return None
