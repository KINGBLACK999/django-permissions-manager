from django.apps import AppConfig

class DjangoPermissionsManagerConfig(AppConfig):
    """Django AppConfig for the permissions manager."""
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'django_permissions_manager.infrastructure.django'
    label = 'django_permissions_manager'
    verbose_name = 'Permissions Manager'

    def ready(self):
        from django.contrib.auth.models import Permission
        from django.db.models.signals import post_delete
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
