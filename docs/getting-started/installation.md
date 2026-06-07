# Installation

## 1. Install the package

The library is not yet published on PyPI. Install it directly from GitHub:

```bash
pip install git+https://github.com/KINGBLACK999/django-permissions-manager.git
```

To pin a specific commit or tag:

```bash
pip install git+https://github.com/KINGBLACK999/django-permissions-manager.git@v0.1.0
```

---

## 2. Add to `INSTALLED_APPS`

```python title="settings.py"
INSTALLED_APPS = [
    "django.contrib.auth",
    "django.contrib.contenttypes",
    # ...
    "django_permissions_manager.infrastructure.django",
]
```

---

## 3. Register the authentication backend

```python title="settings.py"
AUTHENTICATION_BACKENDS = [
    "django.contrib.auth.backends.ModelBackend",
    "django_permissions_manager.infrastructure.django.views.backends.PermissionsManagerBackend",
]
```

!!! tip
    Keep `ModelBackend` first. `PermissionsManagerBackend` handles permission checks
    through the RBAC engine; `ModelBackend` keeps the rest of Django's auth working normally.

---

## 4. Run migrations

```bash
python manage.py migrate
```

This creates three tables in your database:

| Table | Purpose |
|---|---|
| `pm_roles` | Stores roles (global and entity-scoped) |
| `pm_user_roles` | Stores user-to-role assignments |
| `pm_permission_groups` | Stores named groups of permissions |

---

## 5. (Optional) Create default roles

```bash
python manage.py create_default_roles
```

Creates the roles defined in [`PERMISSIONS_MANAGER_DEFAULT_ROLES`](../configuration/default-roles.md).
By default that is **Administrator**, **Editor** and **Viewer**.
