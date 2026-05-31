from django.contrib.auth.backends import BaseBackend
from django.core.cache import cache
from ..services import get_check_permission_use_case
from ..settings import app_settings

# Cache key templates
_USER_VERSION_KEY = "pm:uv:{user_id}"
_GLOBAL_VERSION_KEY = "pm:gv"
_PERM_CACHE_KEY = "pm:{gv}:{uv}:{user_id}:{perm}"


def _get_versions(user_id: str) -> tuple[int, int]:
    """Returns (global_version, user_version) used to build the cache key."""
    gv = cache.get(_GLOBAL_VERSION_KEY, 0)
    uv = cache.get(_USER_VERSION_KEY.format(user_id=user_id), 0)
    return gv, uv


def _build_perm_key(user_id: str, perm: str, gv: int, uv: int) -> str:
    return _PERM_CACHE_KEY.format(gv=gv, uv=uv, user_id=user_id, perm=perm)


def invalidate_user_permission_cache(user_id: str) -> None:
    """
    Invalidates all cached permissions for a user.

    Works by incrementing the user's cache version. Old keys become
    unreachable immediately and expire naturally via their TTL.
    Compatible with any Django cache backend (Redis, Memcached, locmem, etc.).
    """
    key = _USER_VERSION_KEY.format(user_id=user_id)
    try:
        cache.incr(key)
    except ValueError:
        # Key doesn't exist yet — initialize at 1
        cache.set(key, 1, timeout=app_settings.CACHE_TIMEOUT * 24)


def invalidate_all_permission_caches() -> None:
    """
    Broad invalidation that affects every user's permission cache.

    Used when a Django auth.Permission is deleted from the system (e.g. on
    migrate). Since we cannot know which users held that permission, we bump
    a global version that is included in all cache keys.
    """
    try:
        cache.incr(_GLOBAL_VERSION_KEY)
    except ValueError:
        cache.set(_GLOBAL_VERSION_KEY, 1, timeout=None)


class PermissionsManagerBackend(BaseBackend):
    """
    Custom Django Authentication Backend.

    Integrates the hexagonal RBAC logic into Django's user.has_perm().
    Uses Django's cache framework for permission caching, making it
    compatible with Redis, Memcached, database cache, and multiple workers.

    Cache invalidation happens automatically via Django signals when:
    - A role is assigned or revoked from a user
    - A role is activated or deactivated
    - A Django auth.Permission is deleted from the system
    """

    def has_perm(self, user_obj, perm, obj=None):
        """
        Check if the user has a specific permission.

        Args:
            user_obj: The Django user instance.
            perm: Permission string in 'app_label.codename' format.
            obj: Optional object for object-level permissions (not used).
        """
        if not user_obj.is_active:
            return False

        if user_obj.is_superuser:
            return True

        if app_settings.CACHE_ENABLED:
            user_id = str(user_obj.id)
            gv, uv = _get_versions(user_id)
            cache_key = _build_perm_key(user_id, perm, gv, uv)
            cached = cache.get(cache_key)
            if cached is not None:
                return cached
            use_case = get_check_permission_use_case()
            result = use_case.execute(user_id=user_id, permission_code=perm)
            cache.set(cache_key, result, timeout=app_settings.CACHE_TIMEOUT)
            return result

        use_case = get_check_permission_use_case()
        return use_case.execute(user_id=str(user_obj.id), permission_code=perm)

    def get_user(self, user_id):
        # We handle authorization only, not authentication (login)
        return None
