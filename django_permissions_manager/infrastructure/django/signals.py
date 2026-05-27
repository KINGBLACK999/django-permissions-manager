from django.dispatch import Signal

# Fired after a role is assigned to a user.
# Provides: user_id (str), role_id (str), assigned_by (str | None)
role_assigned = Signal()

# Fired after a role assignment is removed from a user.
# Provides: user_id (str), role_id (str)
role_revoked = Signal()

# Fired after a role is activated or deactivated.
# Provides: role_id (str), is_active (bool)
role_status_changed = Signal()
