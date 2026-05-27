from django.apps import AppConfig

class DjangoPermissionsManagerConfig(AppConfig):
    """Django AppConfig for the permissions manager."""
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'django_permissions_manager.infrastructure.django'
    label = 'django_permissions_manager'
    verbose_name = 'Permissions Manager'

    def ready(self):
        import django_permissions_manager.infrastructure.django.signals  # noqa: F401
