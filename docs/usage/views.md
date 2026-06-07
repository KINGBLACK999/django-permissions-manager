# Views & Mixins

## `RoleRequiredMixin`

A class-based view mixin that gates access by **role name** instead of a specific permission code.

```python
from django_permissions_manager.infrastructure.django.views.mixins import RoleRequiredMixin
```

### Single role

```python
class AdminDashboardView(RoleRequiredMixin, TemplateView):
    role_required = "Administrator"
    template_name = "admin/dashboard.html"
```

### Multiple roles (any match grants access)

```python
class ContentView(RoleRequiredMixin, TemplateView):
    role_required = ["Editor", "Administrator"]
    template_name = "content/list.html"
```

### No restriction

```python
class PublicView(RoleRequiredMixin, TemplateView):
    role_required = None   # always grants access
    template_name = "public.html"
```

---

### How it works

1. Unauthenticated requests → `handle_no_permission()` (raises `PermissionDenied` by default).
2. For authenticated users, the mixin fetches all roles assigned to the user via `GetUserRolesUseCase`.
3. If the user's role names intersect with `role_required`, access is granted.
4. Otherwise, `handle_no_permission()` is called.

---

## `PermissionsManagerBackend`

The authentication backend that plugs the RBAC engine into Django's `user.has_perm()`.

```python title="settings.py"
AUTHENTICATION_BACKENDS = [
    "django.contrib.auth.backends.ModelBackend",
    "django_permissions_manager.infrastructure.django.views.backends.PermissionsManagerBackend",
]
```

### Behaviour

| User state | Result |
|---|---|
| Inactive | Always `False` |
| Superuser | Always `True` |
| Regular | Checked against active role assignments |

### Cache invalidation helpers

You can manually invalidate the permission cache if needed:

```python
from django_permissions_manager.infrastructure.django.views.backends import (
    invalidate_user_permission_cache,
    invalidate_all_permission_caches,
)

invalidate_user_permission_cache(user_id="42")   # single user
invalidate_all_permission_caches()               # all users
```

These are called automatically by the built-in signal receivers — you rarely need to call them directly.
