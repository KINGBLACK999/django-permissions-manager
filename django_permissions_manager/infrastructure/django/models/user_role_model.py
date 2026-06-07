from django.db import models
from django.conf import settings
import uuid

class UserRoleModel(models.Model):
    """Django ORM model for User-Role assignments."""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='pm_user_roles'
    )
    role = models.ForeignKey(
        'RoleModel',
        on_delete=models.CASCADE,
        related_name='user_assignments'
    )
    assigned_at = models.DateTimeField(auto_now_add=True)
    assigned_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='pm_roles_assigned'
    )

    class Meta:
        db_table = 'pm_user_roles'
        verbose_name = 'User Role Assignment'
        verbose_name_plural = 'User Role Assignments'
        default_permissions = ()
        permissions = [
            ("view_userrole",   "Can view role assignments"),
            ("assign_role",     "Can assign roles to users"),
            ("revoke_role",     "Can revoke role assignments from users"),
        ]
        unique_together = ('user', 'role')

    def __str__(self):
        return f"{self.user} - {self.role.name}"
