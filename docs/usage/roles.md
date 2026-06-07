# Managing Roles

All role operations are available through factory functions in `services.py`.

---

## Create a role

=== "Global role"

    ```python
    from django_permissions_manager.infrastructure.django.services import get_create_role_use_case

    use_case = get_create_role_use_case()
    role = use_case.execute(
        name="Editor",
        description="Can edit content",
        permission_codes=["myapp.change_article", "myapp.view_article"],
    )
    print(role.id, role.name)  # UUID, "Editor"
    ```

=== "Scoped role"

    ```python
    role = use_case.execute(
        name="Company Admin",
        description="Administers a specific company",
        entity_type="Company",
        entity_id="42",
        permission_codes=["myapp.change_article"],
    )
    ```

!!! note "MODE enforcement"
    If `PERMISSIONS_MANAGER_MODE` is set to `"GLOBAL"`, creating a scoped role raises `ValueError`.
    If set to `"ENTITY"`, creating a global role raises `ValueError`.

---

## Update role permissions

Replace the full list of permissions on an existing role:

```python
from django_permissions_manager.application.use_cases.update_role_permissions import UpdateRolePermissionsUseCase
from django_permissions_manager.infrastructure.django.repositories.django_role_repository import DjangoRoleRepository
from django_permissions_manager.infrastructure.django.repositories.django_permission_repository import DjangoPermissionRepository

use_case = UpdateRolePermissionsUseCase(
    role_repository=DjangoRoleRepository(),
    permission_repository=DjangoPermissionRepository(),
)
role = use_case.execute(
    role_id="<uuid>",
    permission_codes=["myapp.view_article", "myapp.add_article"],
)
```

!!! tip
    This **replaces** the permission list entirely. Pass an empty list to clear all permissions.

---

## Activate / deactivate a role

```python
from django_permissions_manager.infrastructure.django.services import get_role_manager
from django_permissions_manager.infrastructure.django.repositories.django_role_repository import DjangoRoleRepository

repo = DjangoRoleRepository()
role = repo.get_by_id("<uuid>")

manager = get_role_manager(repo)
manager.deactivate_role(role)   # Raises SystemRoleDeletionException for system roles
manager.activate_role(role)
```

Deactivating a role immediately prevents its permissions from being granted to users.
The `role_status_changed` signal is fired and the permission cache is invalidated.

---

## Assign a role to a user

```python
from django_permissions_manager.infrastructure.django.services import get_assign_role_use_case

use_case = get_assign_role_use_case()
assignment = use_case.execute(
    user_id=str(user.id),
    role_id="<uuid>",
    assigned_by_id=str(request.user.id),  # optional
)
```

---

## Revoke a role from a user

```python
from django_permissions_manager.infrastructure.django.services import get_remove_role_use_case

use_case = get_remove_role_use_case()
use_case.execute(user_role_id="<assignment-uuid>")
```

---

## List all roles for a user

```python
from django_permissions_manager.infrastructure.django.services import get_user_roles_use_case

use_case = get_user_roles_use_case()
roles = use_case.execute(user_id=str(user.id))

for r in roles:
    print(r.role_name, r.assigned_at)
```
