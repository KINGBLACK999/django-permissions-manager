# Quick Start

After [installing the library](installation.md), here is everything you need to get roles and permissions working.

---

## Create a role

```python
from django_permissions_manager.infrastructure.django.services import get_create_role_use_case

use_case = get_create_role_use_case()

# Global role (applies system-wide)
role = use_case.execute(
    name="Editor",
    description="Can edit content",
    permission_codes=["myapp.change_article", "myapp.view_article"],
)

# Scoped role (tied to a specific entity)
scoped_role = use_case.execute(
    name="Manager",
    description="Manages a specific company",
    entity_type="Company",
    entity_id="42",
    permission_codes=["myapp.change_article"],
)
```

---

## Assign a role to a user

```python
from django_permissions_manager.infrastructure.django.services import get_assign_role_use_case

use_case = get_assign_role_use_case()
use_case.execute(user_id=str(request.user.id), role_id=role.id)
```

---

## Check a permission

Once the backend is registered, use Django's standard API anywhere:

```python
user.has_perm("myapp.change_article")  # True / False
```

This works transparently with all Django permission tools:

```python
# Function-based views
@permission_required("myapp.change_article")
def my_view(request): ...

# Class-based views
from django.contrib.auth.mixins import PermissionRequiredMixin

class MyView(PermissionRequiredMixin, View):
    permission_required = "myapp.change_article"

# DRF
from rest_framework.permissions import DjangoModelPermissions
```

---

## Require a role by name

Use `RoleRequiredMixin` when you want to gate access by role name rather than a specific permission code:

```python
from django_permissions_manager.infrastructure.django.views.mixins import RoleRequiredMixin

class DashboardView(RoleRequiredMixin, TemplateView):
    role_required = "Editor"
    template_name = "dashboard.html"
```

---

## Next steps

- [Configure the library](../configuration/settings.md) for your project.
- [Manage permission groups](../usage/permission-groups.md) for bulk assignment.
- [Hook into signals](../usage/signals.md) to react to role changes.
