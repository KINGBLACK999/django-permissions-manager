# Use Cases

Use cases live in `django_permissions_manager.application.use_cases`. Each one is a single-responsibility class with an `execute()` method. The easiest way to get a wired instance is through the [service factory functions](services.md).

---

## `CreateRoleUseCase`

Creates a global or entity-scoped role.

**Constructor dependencies**

| Parameter | Type | Description |
|---|---|---|
| `role_repository` | `RoleRepository` | Persists the role |
| `permission_repository` | `PermissionReadRepository` | Resolves permission codes |
| `role_manager` | `RoleManager` | Enforces name uniqueness |
| `entity_service` | `EntityService \| None` | Optional — validates entity existence |
| `mode` | `str` | `"GLOBAL"`, `"ENTITY"`, or `"BOTH"` (default) |

**`execute()` parameters**

| Parameter | Type | Default | Description |
|---|---|---|---|
| `name` | `str` | required | Role display name |
| `description` | `str` | `""` | Human-readable description |
| `entity_type` | `str \| None` | `None` | Entity type for scoped roles |
| `entity_id` | `str \| None` | `None` | Entity ID for scoped roles |
| `permission_codes` | `list[str] \| None` | `None` | Permission codes to assign |
| `is_system_role` | `bool` | `False` | Prevents deactivation |

**Returns** `RoleDTO` · **Raises** `RoleAlreadyExistsException`, `ValueError`

---

## `UpdateRolePermissionsUseCase`

Replaces the full permission list on an existing role.

**`execute()` parameters**

| Parameter | Type | Description |
|---|---|---|
| `role_id` | `str` | UUID of the role to update |
| `permission_codes` | `list[str]` | New full list of permission codes (replaces existing) |

**Returns** `RoleDTO` · **Raises** `ValueError` if the role is not found

!!! tip
    Pass an empty list to clear all permissions from the role.

---

## `AssignRoleToUserUseCase`

Assigns a role to a user. Fires `role_assigned` signal.

**`execute()` parameters**

| Parameter | Type | Default | Description |
|---|---|---|---|
| `user_id` | `str` | required | ID of the user |
| `role_id` | `str` | required | UUID of the role |
| `assigned_by_id` | `str \| None` | `None` | ID of the assigning user |

**Returns** `UserRoleDTO` · **Raises** `ValueError` if the role is not found

---

## `RemoveRoleFromUserUseCase`

Removes a role assignment. Fires `role_revoked` signal.

**`execute()` parameters**

| Parameter | Type | Description |
|---|---|---|
| `user_role_id` | `str` | UUID of the assignment to remove |

**Returns** `None` · **Raises** `ValueError` if the assignment is not found

---

## `GetUserRolesUseCase`

Returns all role assignments for a user.

**`execute()` parameters**

| Parameter | Type | Description |
|---|---|---|
| `user_id` | `str` | ID of the user |

**Returns** `list[UserRoleDTO]`

---

## `CheckUserPermissionUseCase`

Checks whether a user has a specific permission through their roles.

**`execute()` parameters**

| Parameter | Type | Description |
|---|---|---|
| `user_id` | `str` | ID of the user |
| `permission_code` | `str` | Permission code in `app_label.codename` format |

**Returns** `bool`

---

## `CreatePermissionGroupUseCase`

Creates a named group of permissions.

**`execute()` parameters**

| Parameter | Type | Default | Description |
|---|---|---|---|
| `name` | `str` | required | Unique group name |
| `description` | `str` | `""` | Human-readable description |
| `permission_codes` | `list[str] \| None` | `None` | Permissions to include |

**Returns** `PermissionGroupDTO` · **Raises** `ValueError` if the name already exists

---

## `AssignPermissionGroupToRoleUseCase`

Adds all permissions from a group into a role. Existing permissions are kept; duplicates are ignored.

**`execute()` parameters**

| Parameter | Type | Description |
|---|---|---|
| `role_id` | `str` | UUID of the role |
| `group_id` | `str` | UUID of the permission group |

**Returns** `RoleDTO` · **Raises** `ValueError` if the role or group is not found

---

## `CreateDefaultRolesUseCase`

Creates roles from a list of dicts. Roles that already exist are skipped.

**`execute()` parameters**

| Parameter | Type | Description |
|---|---|---|
| `default_roles` | `list[dict]` | List of `{"name": ..., "description": ...}` entries |

**Returns** `None`

This use case is called internally by `python manage.py create_default_roles`.
