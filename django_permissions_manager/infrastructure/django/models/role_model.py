import uuid
from django.db import models
from django.conf import settings

class RoleModel(models.Model):
    """Django ORM model for Roles."""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    
    # Entity context for multi-tenancy or scoped roles
    entity_type = models.CharField(max_length=100, null=True, blank=True, db_index=True)
    entity_id = models.CharField(max_length=100, null=True, blank=True, db_index=True)
    
    permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='custom_roles',
        blank=True
    )
    
    is_active = models.BooleanField(default=True)
    is_system_role = models.BooleanField(default=False)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'pm_roles'
        verbose_name = 'Role'
        verbose_name_plural = 'Roles'
        constraints = [
            # Constraint for entity-specific roles
            models.UniqueConstraint(
                fields=['name', 'entity_type', 'entity_id'],
                name='unique_role_name_per_entity',
                condition=models.Q(entity_type__isnull=False, entity_id__isnull=False)
            ),
            # Constraint for global roles (where entity is null)
            models.UniqueConstraint(
                fields=['name'],
                name='unique_global_role_name',
                condition=models.Q(entity_type__isnull=True, entity_id__isnull=True)
            )
        ]

    def __str__(self):
        if self.entity_type and self.entity_id:
            return f"{self.name} ({self.entity_type}:{self.entity_id})"
        return f"{self.name} (Global)"
