# Checking Permissions

Once `PermissionsManagerBackend` is registered, permission checks go through the RBAC engine automatically. No changes are needed in your views.

---

## Standard Django API

```python
user.has_perm("myapp.view_article")     # True / False
user.has_perm("myapp.change_article")   # True / False
```

---

## Function-based views

```python
from django.contrib.auth.decorators import permission_required

@permission_required("myapp.change_article")
def edit_article(request, pk): ...
```

---

## Class-based views

```python
from django.contrib.auth.mixins import PermissionRequiredMixin

class EditArticleView(PermissionRequiredMixin, UpdateView):
    permission_required = "myapp.change_article"
    model = Article
```

---

## Django REST Framework

```python
from rest_framework.permissions import DjangoModelPermissions
from rest_framework.views import APIView

class ArticleView(APIView):
    permission_classes = [DjangoModelPermissions]
```

---

## Django Ninja

```python
from ninja import Router
from django.contrib.auth.decorators import permission_required

router = Router()

@router.get("/articles", auth=django_auth)
@permission_required("myapp.view_article")
def list_articles(request): ...
```

---

## Checking programmatically (use case)

Use `CheckUserPermissionUseCase` directly when you need the result as a boolean without going through a view:

```python
from django_permissions_manager.infrastructure.django.services import get_check_permission_use_case

use_case = get_check_permission_use_case()
has_access = use_case.execute(
    user_id=str(user.id),
    permission_code="myapp.change_article",
)
```

---

## How the backend works

1. Inactive users are always denied.
2. Superusers are always allowed.
3. For regular users, the backend fetches all their active role assignments, collects the associated permissions, and checks for a match.
4. Results are cached per `(user_id, permission_code)` key for `CACHE_TIMEOUT` seconds (default 1 hour).

See [Settings](../configuration/settings.md) for cache configuration.
