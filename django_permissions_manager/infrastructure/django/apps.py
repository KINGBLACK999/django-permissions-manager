import warnings

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

        # Optional audit log integration — only activated when both
        # PERMISSIONS_MANAGER_AUDIT_LOG = True and django-auditlog is installed.
        _setup_audit_log()


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


def _setup_audit_log():
    """Optionally register library models with django-auditlog.

    Only activates when ALL three conditions are met:
      1. PERMISSIONS_MANAGER_AUDIT_LOG = True in project settings.
      2. 'auditlog' is in INSTALLED_APPS.
      3. django-auditlog is installed (importable).

    If condition 1 is True but conditions 2 or 3 fail, a RuntimeWarning is
    emitted so the developer knows the setting has no effect.
    """
    from .settings import app_settings

    if not app_settings.AUDIT_LOG:
        return  # opted out (default) — nothing to do

    # Check django-auditlog is importable.
    try:
        from auditlog.registry import auditlog as auditlog_registry
    except ImportError:
        warnings.warn(
            "PERMISSIONS_MANAGER_AUDIT_LOG is True but django-auditlog is not "
            "installed. Install it with: pip install django-auditlog",
            RuntimeWarning,
            stacklevel=2,
        )
        return

    # Check 'auditlog' is in INSTALLED_APPS.
    from django.apps import apps as django_apps
    if not django_apps.is_installed('auditlog'):
        warnings.warn(
            "PERMISSIONS_MANAGER_AUDIT_LOG is True but 'auditlog' is not in "
            "INSTALLED_APPS. Add it to enable audit logging.",
            RuntimeWarning,
            stacklevel=2,
        )
        return

    # All conditions met — register models.
    from .models.role_model import RoleModel
    from .models.user_role_model import UserRoleModel

    auditlog_registry.register(RoleModel)
    auditlog_registry.register(UserRoleModel)
