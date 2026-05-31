# django-permissions-manager

Role-based permission management (RBAC) for Django, built with hexagonal architecture and DDD.

Roles can be **global** (system-wide) or **scoped to an entity** (e.g. a company or tenant). Permission checks integrate transparently into Django's standard `user.has_perm()` API via a custom authentication backend.

The library provides the full RBAC engine — domain logic, repositories, use cases — but **does not expose HTTP endpoints**. You build your own views using whatever stack you prefer (plain Django, DRF, Django Ninja, etc.) and call the provided use cases directly.

---

## Requirements

- Python >= 3.11
- Django >= 6.0

---

## Installation

```bash
pip install django-permissions-manager
```

---

## Quick start

### 1. Add to `INSTALLED_APPS`

```python
INSTALLED_APPS = [
    ...
    "django_permissions_manager.infrastructure.django",
]
```

### 2. Register the authentication backend

```python
AUTHENTICATION_BACKENDS = [
    "django.contrib.auth.backends.ModelBackend",
    "django_permissions_manager.infrastructure.django.views.backends.PermissionsManagerBackend",
]
```

### 3. Run migrations

```bash
python manage.py migrate
```

This creates three tables: `pm_roles`, `pm_user_roles`, and `pm_permission_groups`.

### 4. (Optional) Create default roles

```bash
python manage.py create_default_roles
```

---

## Configuration

All settings are optional and have defaults. Override them in your project's `settings.py` using the `PERMISSIONS_MANAGER_` prefix.

| Setting | Default | Description |
|---|---|---|
| `MODE` | `"BOTH"` | Which role types are allowed. Options: `"GLOBAL"`, `"ENTITY"`, `"BOTH"` |
| `CACHE_ENABLED` | `True` | Enable permission result caching |
| `CACHE_TIMEOUT` | `3600` | Cache TTL in seconds |
| `USER_MODEL` | `settings.AUTH_USER_MODEL` | The user model to associate roles with |
| `DEFAULT_ROLES` | See below | Roles created by `create_default_roles` |

**Example:**

```python
PERMISSIONS_MANAGER_MODE = "BOTH"
PERMISSIONS_MANAGER_CACHE_ENABLED = True
PERMISSIONS_MANAGER_CACHE_TIMEOUT = 3600

PERMISSIONS_MANAGER_DEFAULT_ROLES = [
    {"name": "Administrator", "description": "Full system access"},
    {"name": "Editor", "description": "Can edit content but not manage users"},
    {"name": "Viewer", "description": "Read-only access"},
]
```

### Cache backend

`CACHE_ENABLED` uses Django's cache framework, so it works with any configured backend — locmem (default), Redis, Memcached, or database cache. No extra setup required.

The cache is invalidated automatically via Django signals whenever a role is assigned, revoked, or its status changes.

---

## Usage

### Checking permissions

Once the backend is registered, use Django's standard API anywhere in your code:

```python
user.has_perm("myapp.view_report")   # True / False
```

`@permission_required`, `PermissionRequiredMixin`, and DRF's `DjangoModelPermissions` all work out of the box — no changes needed.

### Requiring a role by name

Use `RoleRequiredMixin` in class-based views to gate access by role name instead of a specific permission code:

```python
from django_permissions_manager.infrastructure.django.views.mixins import RoleRequiredMixin

class ReportsView(RoleRequiredMixin, TemplateView):
    role_required = "Editor"                          # single role
    # role_required = ["Editor", "Administrator"]     # any of these
    template_name = "reports.html"
```

### Signals

Hook into the role assignment and status lifecycle:

```python
from django.dispatch import receiver
from django_permissions_manager.infrastructure.django.signals import (
    role_assigned,
    role_revoked,
    role_status_changed,
)

@receiver(role_assigned)
def on_role_assigned(sender, user_id, role_id, assigned_by, **kwargs):
    ...

@receiver(role_revoked)
def on_role_revoked(sender, user_id, role_id, **kwargs):
    ...

@receiver(role_status_changed)
def on_role_status_changed(sender, role_id, is_active, **kwargs):
    ...
```

---

## Building your own views

Import the use case factory functions from `services` and call them from your views. Each function returns a fully wired use case instance ready to execute.

```python
from django_permissions_manager.infrastructure.django.services import (
    get_create_role_use_case,
    get_assign_role_use_case,
    get_remove_role_use_case,
    get_user_roles_use_case,
    get_create_permission_group_use_case,
    get_assign_permission_group_to_role_use_case,
    get_role_manager,
)
```

### Plain Django views

```python
import json
from django.http import JsonResponse
from django.views import View
from django_permissions_manager.infrastructure.django.services import (
    get_create_role_use_case,
    get_assign_role_use_case,
    get_user_roles_use_case,
)

class RoleListCreateView(View):
    def post(self, request):
        data = json.loads(request.body)
        try:
            use_case = get_create_role_use_case()
            dto = use_case.execute(
                name=data["name"],
                description=data.get("description", ""),
                permission_codes=data.get("permission_codes", []),
            )
        except ValueError as e:
            return JsonResponse({"detail": str(e)}, status=400)
        return JsonResponse({"id": dto.id, "name": dto.name}, status=201)


class UserRoleListCreateView(View):
    def get(self, request, user_id):
        use_case = get_user_roles_use_case()
        roles = use_case.execute(user_id=user_id)
        data = [{"role_id": r.role_id, "role_name": r.role_name} for r in roles]
        return JsonResponse(data, safe=False)

    def post(self, request, user_id):
        data = json.loads(request.body)
        try:
            use_case = get_assign_role_use_case()
            dto = use_case.execute(user_id=user_id, role_id=data["role_id"])
        except ValueError as e:
            return JsonResponse({"detail": str(e)}, status=400)
        return JsonResponse({"id": dto.id, "role_name": dto.role_name}, status=201)
```

### With Django REST Framework

```python
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django_permissions_manager.infrastructure.django.services import (
    get_create_role_use_case,
    get_user_roles_use_case,
)

class RoleView(APIView):
    def post(self, request):
        try:
            use_case = get_create_role_use_case()
            dto = use_case.execute(
                name=request.data["name"],
                description=request.data.get("description", ""),
                permission_codes=request.data.get("permission_codes", []),
            )
        except ValueError as e:
            return Response({"detail": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        return Response({"id": dto.id, "name": dto.name}, status=status.HTTP_201_CREATED)


class UserRolesView(APIView):
    def get(self, request, user_id):
        use_case = get_user_roles_use_case()
        roles = use_case.execute(user_id=user_id)
        return Response([{"role_id": r.role_id, "role_name": r.role_name} for r in roles])
```

### With Django Ninja

```python
from ninja import Router
from django_permissions_manager.infrastructure.django.services import (
    get_create_role_use_case,
    get_user_roles_use_case,
)

router = Router()

@router.post("/roles")
def create_role(request, name: str, description: str = "", permission_codes: list[str] = []):
    use_case = get_create_role_use_case()
    dto = use_case.execute(name=name, description=description, permission_codes=permission_codes)
    return {"id": dto.id, "name": dto.name}

@router.get("/users/{user_id}/roles")
def list_user_roles(request, user_id: str):
    use_case = get_user_roles_use_case()
    roles = use_case.execute(user_id=user_id)
    return [{"role_id": r.role_id, "role_name": r.role_name} for r in roles]
```

### Activate / deactivate a role

```python
from django_permissions_manager.infrastructure.django.services import get_role_manager
from django_permissions_manager.infrastructure.django.repositories.django_role_repository import DjangoRoleRepository

def activate_role(role_id: str):
    repo = DjangoRoleRepository()
    role = repo.get_by_id(role_id)
    if not role:
        raise ValueError("Role not found")
    get_role_manager(repo).activate_role(role)

def deactivate_role(role_id: str):
    repo = DjangoRoleRepository()
    role = repo.get_by_id(role_id)
    if not role:
        raise ValueError("Role not found")
    get_role_manager(repo).deactivate_role(role)   # raises if system role
```

---

## Available use cases

| Factory function | What it does |
|---|---|
| `get_create_role_use_case()` | Creates a global or entity-scoped role |
| `get_assign_role_use_case()` | Assigns a role to a user |
| `get_remove_role_use_case()` | Removes a role assignment from a user |
| `get_user_roles_use_case()` | Lists all roles assigned to a user |
| `get_create_permission_group_use_case()` | Creates a named group of permissions |
| `get_assign_permission_group_to_role_use_case()` | Adds all permissions from a group into a role |
| `get_role_manager()` | Activates / deactivates roles and enforces name uniqueness |

---

## Architecture

The library follows hexagonal architecture (Ports & Adapters) with DDD:

```
django_permissions_manager/
├── domain/             # Entities, value objects, repository interfaces, domain services
│   ├── entities/       # Role, Permission, PermissionGroup, UserRole
│   ├── value_objects/  # RoleName, PermissionCode, EntityReference, UserId
│   ├── repositories/   # Abstract repository interfaces (ports)
│   └── services/       # PermissionChecker, RoleManager, RoleFactory
├── application/        # Use cases and DTOs
│   ├── use_cases/      # CreateRole, AssignRole, CheckPermission, etc.
│   └── dto/            # RoleDTO, UserRoleDTO, PermissionDTO
└── infrastructure/
    └── django/         # Django ORM models, repositories, signals, auth backend
        ├── models/     # RoleModel (pm_roles), UserRoleModel (pm_user_roles), PermissionGroupModel
        ├── repositories/
        ├── mappers/
        ├── views/      # PermissionsManagerBackend, RoleRequiredMixin
        └── migrations/
```

Domain code has no knowledge of Django or any persistence technology. Infrastructure adapters implement the repository interfaces defined in the domain.

---

## License

MIT
