# Settings Reference

All settings are optional and have defaults. Override them in your project's `settings.py` using the `PERMISSIONS_MANAGER_` prefix.

---

## Full example

```python title="settings.py"
PERMISSIONS_MANAGER_MODE = "BOTH"
PERMISSIONS_MANAGER_CACHE_ENABLED = True
PERMISSIONS_MANAGER_CACHE_TIMEOUT = 3600
PERMISSIONS_MANAGER_USER_MODEL = "auth.User"

PERMISSIONS_MANAGER_DEFAULT_ROLES = [
    {"name": "Administrator", "description": "Full system access"},
    {"name": "Editor",        "description": "Can edit content but not manage users"},
    {"name": "Viewer",        "description": "Read-only access"},
]

PERMISSIONS_MANAGER_PERMISSION_LABELS = {
    "change_role": "Can modify a role's name and permissions",
    "assign_role": "Can assign roles to users",
}
```

---

## Reference

### `MODE`

Controls which types of roles the library allows to be created.

| Value | Description |
|---|---|
| `"GLOBAL"` | Only global roles (no entity scope) |
| `"ENTITY"` | Only entity-scoped roles |
| `"BOTH"` *(default)* | Both global and scoped roles |

```python
PERMISSIONS_MANAGER_MODE = "BOTH"
```

!!! warning
    If you switch from `BOTH` to `GLOBAL` or `ENTITY` after roles already exist,
    existing roles in the database are not affected — only new role creation is blocked.

---

### `CACHE_ENABLED`

Enables caching of permission check results.

| Type | Default |
|---|---|
| `bool` | `True` |

```python
PERMISSIONS_MANAGER_CACHE_ENABLED = True
```

The cache is automatically invalidated when:

- A role is assigned to a user.
- A role is revoked from a user.
- A role is activated or deactivated.

---

### `CACHE_TIMEOUT`

Time-to-live for cached permission results, in seconds.

| Type | Default |
|---|---|
| `int` | `3600` (1 hour) |

```python
PERMISSIONS_MANAGER_CACHE_TIMEOUT = 3600
```

Works with any Django cache backend — locmem (default), Redis, Memcached, or database cache.

---

### `USER_MODEL`

The user model to associate role assignments with.

| Type | Default |
|---|---|
| `str` | `settings.AUTH_USER_MODEL` |

```python
PERMISSIONS_MANAGER_USER_MODEL = "auth.User"
```

You only need to set this if you use a custom user model with a non-standard path.

---

### `DEFAULT_ROLES`

List of roles created by `python manage.py create_default_roles`.

| Type | Default |
|---|---|
| `list[dict]` | Administrator, Editor, Viewer |

See [Default Roles](default-roles.md) for full documentation.

---

### `PERMISSION_LABELS`

Dictionary mapping permission codenames to custom human-readable labels.
Applied automatically after every `manage.py migrate`.

| Type | Default |
|---|---|
| `dict[str, str]` | `{}` |

See [Permission Labels](permission-labels.md) for full documentation.
