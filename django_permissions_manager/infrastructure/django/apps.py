from django.apps import AppConfig

class DjangoPermissionsManagerConfig(AppConfig):
    """Django AppConfig for the permissions manager."""
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'django_permissions_manager.infrastructure.django'
    label = 'django_permissions_manager'
    verbose_name = 'Permissions Manager'

    def ready(self):
        from django.contrib.auth.models import Permission
        from django.db.models.signals import post_delete, post_migrate
        from .signals import role_assigned, role_revoked, role_status_changed
        from .views.backends import (
            invalidate_user_permission_cache,
            invalidate_all_permission_caches,
        )

        role_assigned.connect(
            lambda sender, user_id, **kw: invalidate_user_permission_cache(user_id)
        )
        role_revoked.connect(
            lambda sender, user_id, **kw: invalidate_user_permission_cache(user_id)
        )
        role_status_changed.connect(
            lambda sender, **kw: invalidate_all_permission_caches()
        )
        post_delete.connect(
            lambda sender, **kw: invalidate_all_permission_caches(),
            sender=Permission,
        )
        # Apply project-level permission label overrides after every migration run.
        # Runs after django.contrib.auth's create_permissions, so labels are always
        # applied on top of freshly created permissions.
        post_migrate.connect(_apply_permission_labels, sender=self)


def _apply_permission_labels(sender, **kwargs):
    """Signal handler: resolve imports and delegate to the pure helper."""
    from django.contrib.auth.models import Permission
    from .settings import app_settings

    _update_permission_labels(Permission, app_settings.PERMISSION_LABELS)


def _update_permission_labels(permission_model, labels):
    """Update permission names based on a codename->label mapping.

    Kept as a pure, dependency-injected function so it can be tested without
    touching the database or patching module-level names.

    Args:
        permission_model: The Django Permission model class (or a mock in tests).
        labels: Dict mapping codename strings to human-readable label strings.
    """
    if not labels:
        return

    for codename, name in labels.items():
        permission_model.objects.filter(
            content_type__app_label='django_permissions_manager',
            codename=codename,
        ).update(name=name)
