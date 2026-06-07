# Permission Groups

Permission groups let you bundle related permissions together under a name and then assign the whole bundle to one or more roles at once.

---

## Create a group

```python
from django_permissions_manager.infrastructure.django.services import get_create_permission_group_use_case

use_case = get_create_permission_group_use_case()
group = use_case.execute(
    name="Content Management",
    description="Permissions for managing articles and media",
    permission_codes=[
        "myapp.view_article",
        "myapp.add_article",
        "myapp.change_article",
        "myapp.delete_article",
    ],
)
print(group.id, group.name)
```

---

## Assign a group to a role

Adds all permissions from the group to the role. Existing permissions on the role are kept — duplicates are ignored.

```python
from django_permissions_manager.infrastructure.django.services import (
    get_assign_permission_group_to_role_use_case,
)

use_case = get_assign_permission_group_to_role_use_case()
use_case.execute(role_id="<uuid>", group_id=group.id)
```

---

## Typical workflow

```python
# 1. Create a group with a set of permissions
group_uc = get_create_permission_group_use_case()
group = group_uc.execute(
    name="Blog Editor",
    permission_codes=["blog.add_post", "blog.change_post", "blog.view_post"],
)

# 2. Create a role
role_uc = get_create_role_use_case()
role = role_uc.execute(name="Blog Editor", description="Manages blog posts")

# 3. Assign the group to the role
assign_uc = get_assign_permission_group_to_role_use_case()
assign_uc.execute(role_id=role.id, group_id=group.id)

# 4. Assign the role to a user
user_uc = get_assign_role_use_case()
user_uc.execute(user_id=str(user.id), role_id=role.id)
```

---

## When to use groups vs. direct permissions

| Scenario | Recommendation |
|---|---|
| Many roles share the same set of permissions | Define a group and assign it to each role |
| A role has a unique, one-off set of permissions | Assign permissions directly via `update_role_permissions` |
| Permissions change frequently across many roles | Keep a group — update the group once, all roles inherit the change via re-assignment |
