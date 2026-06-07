# Default Roles

The `create_default_roles` management command seeds your database with a base set of roles.
Configure them with `PERMISSIONS_MANAGER_DEFAULT_ROLES`.

---

## Running the command

```bash
python manage.py create_default_roles
```

- Roles that already exist are **skipped** — safe to run multiple times.
- All seeded roles are flagged as `is_system_role=True`, which prevents them from being deactivated accidentally.

---

## Configuration

```python title="settings.py"
PERMISSIONS_MANAGER_DEFAULT_ROLES = [
    {"name": "Administrator", "description": "Full system access"},
    {"name": "Editor",        "description": "Can edit content but not manage users"},
    {"name": "Viewer",        "description": "Read-only access"},
]
```

Each entry requires a `name` key. The `description` key is optional.

---

## Custom roles

Replace the defaults with whatever your project needs:

```python title="settings.py"
PERMISSIONS_MANAGER_DEFAULT_ROLES = [
    {"name": "Owner",        "description": "Full access to all resources"},
    {"name": "Contributor",  "description": "Can create and edit content"},
    {"name": "Reviewer",     "description": "Can approve or reject submissions"},
    {"name": "Guest",        "description": "Read-only access"},
]
```

---

## Assigning permissions to default roles

The management command only creates the roles — it does not assign permissions to them.
Use the `UpdateRolePermissionsUseCase` or the Django admin after seeding:

```python
from django_permissions_manager.infrastructure.django.services import get_create_role_use_case
from django_permissions_manager.infrastructure.django.repositories.django_role_repository import DjangoRoleRepository

repo = DjangoRoleRepository()
role = repo.get_by_name("Editor")

from django_permissions_manager.application.use_cases.update_role_permissions import UpdateRolePermissionsUseCase
from django_permissions_manager.infrastructure.django.repositories.django_permission_repository import DjangoPermissionRepository

use_case = UpdateRolePermissionsUseCase(
    role_repository=repo,
    permission_repository=DjangoPermissionRepository(),
)
use_case.execute(
    role_id=role.id,
    permission_codes=["myapp.change_article", "myapp.view_article"],
)
```
