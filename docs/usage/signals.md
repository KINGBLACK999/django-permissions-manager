# Signals

The library fires Django signals at key points in the role lifecycle. Use them to integrate with audit logs, notification systems, or any other side effects your project needs.

---

## Available signals

```python
from django_permissions_manager.infrastructure.django.signals import (
    role_assigned,
    role_revoked,
    role_status_changed,
)
```

---

## `role_assigned`

Fired when a role is assigned to a user.

| Argument | Type | Description |
|---|---|---|
| `sender` | `AssignRoleToUserUseCase` | The use case class |
| `user_id` | `str` | ID of the user who received the role |
| `role_id` | `str` | ID of the assigned role |
| `assigned_by` | `str \| None` | ID of the user who performed the assignment |

```python
from django.dispatch import receiver
from django_permissions_manager.infrastructure.django.signals import role_assigned

@receiver(role_assigned)
def on_role_assigned(sender, user_id, role_id, assigned_by, **kwargs):
    print(f"User {user_id} was assigned role {role_id} by {assigned_by}")
```

---

## `role_revoked`

Fired when a role assignment is removed from a user.

| Argument | Type | Description |
|---|---|---|
| `sender` | `RemoveRoleFromUserUseCase` | The use case class |
| `user_id` | `str` | ID of the user who lost the role |
| `role_id` | `str` | ID of the revoked role |

```python
@receiver(role_revoked)
def on_role_revoked(sender, user_id, role_id, **kwargs):
    print(f"Role {role_id} was revoked from user {user_id}")
```

---

## `role_status_changed`

Fired when a role is activated or deactivated.

| Argument | Type | Description |
|---|---|---|
| `sender` | `RoleManager` | The domain service class |
| `role_id` | `str` | ID of the role whose status changed |
| `is_active` | `bool` | New status (`True` = active, `False` = inactive) |

```python
@receiver(role_status_changed)
def on_role_status_changed(sender, role_id, is_active, **kwargs):
    status = "activated" if is_active else "deactivated"
    print(f"Role {role_id} was {status}")
```

---

## Cache invalidation

The library connects its own receivers to these signals internally to invalidate the permission cache automatically:

- `role_assigned` → invalidates the cache for the affected user.
- `role_revoked` → invalidates the cache for the affected user.
- `role_status_changed` → invalidates the **entire** permission cache (all users), since a role status change affects every user who holds that role.

Your own receivers run alongside the built-in ones.
