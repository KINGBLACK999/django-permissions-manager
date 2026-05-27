from django.db import models
import uuid

class PermissionGroupModel(models.Model):
    """Django ORM model for grouping permissions together."""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255, unique=True)
    description = models.TextField(blank=True)
    permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='pm_permission_groups',
        blank=True
    )

    class Meta:
        db_table = 'pm_permission_groups'
        verbose_name = 'Permission Group'
        verbose_name_plural = 'Permission Groups'

    def __str__(self):
        return self.name
