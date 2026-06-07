# Services

Factory functions in `django_permissions_manager.infrastructure.django.services` return fully wired use case instances. Import and call them directly in your views.

```python
from django_permissions_manager.infrastructure.django.services import (
    get_create_role_use_case,
    get_assign_role_use_case,
    get_remove_role_use_case,
    get_user_roles_use_case,
    get_check_permission_use_case,
    get_create_permission_group_use_case,
    get_assign_permission_group_to_role_use_case,
    get_role_manager,
)
```

---

## Reference

### `get_create_role_use_case()`

Returns a `CreateRoleUseCase` wired with `DjangoRoleRepository`, `DjangoPermissionRepository`, `RoleManager`, and the configured `MODE`.

```python
role = get_create_role_use_case().execute(name="Editor", permission_codes=[...])
```

---

### `get_assign_role_use_case()`

Returns an `AssignRoleToUserUseCase` wired with `DjangoUserRoleRepository`, `DjangoRoleRepository`, and the `role_assigned` signal.

```python
get_assign_role_use_case().execute(user_id=str(user.id), role_id=role.id)
```

---

### `get_remove_role_use_case()`

Returns a `RemoveRoleFromUserUseCase` wired with `DjangoUserRoleRepository` and the `role_revoked` signal.

```python
get_remove_role_use_case().execute(user_role_id="<uuid>")
```

---

### `get_user_roles_use_case()`

Returns a `GetUserRolesUseCase` wired with `DjangoUserRoleRepository`.

```python
roles = get_user_roles_use_case().execute(user_id=str(user.id))
```

---

### `get_check_permission_use_case()`

Returns a `CheckUserPermissionUseCase` wired with `DjangoUserRoleRepository` and `PermissionChecker`.

```python
allowed = get_check_permission_use_case().execute(
    user_id=str(user.id),
    permission_code="myapp.change_article",
)
```

---

### `get_create_permission_group_use_case()`

Returns a `CreatePermissionGroupUseCase` wired with `DjangoPermissionGroupRepository` and `DjangoPermissionRepository`.

```python
group = get_create_permission_group_use_case().execute(
    name="Content Management",
    permission_codes=["myapp.add_article", "myapp.change_article"],
)
```

---

### `get_assign_permission_group_to_role_use_case()`

Returns an `AssignPermissionGroupToRoleUseCase` wired with `DjangoRoleRepository` and `DjangoPermissionGroupRepository`.

```python
get_assign_permission_group_to_role_use_case().execute(
    role_id=role.id,
    group_id=group.id,
)
```

---

### `get_role_manager(role_repo=None)`

Returns a `RoleManager` wired with the `role_status_changed` signal.

| Parameter | Type | Default | Description |
|---|---|---|---|
| `role_repo` | `DjangoRoleRepository \| None` | `None` | Pass an existing repo to avoid a second instantiation |

```python
from django_permissions_manager.infrastructure.django.repositories.django_role_repository import DjangoRoleRepository

repo = DjangoRoleRepository()
role = repo.get_by_id("<uuid>")

manager = get_role_manager(repo)
manager.deactivate_role(role)
```
