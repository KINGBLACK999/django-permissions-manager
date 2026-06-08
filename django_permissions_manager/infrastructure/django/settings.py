from django.conf import settings

# Library settings with default values
DEFAULTS = {
    'MODE': 'BOTH',  # Options: 'GLOBAL', 'ENTITY', 'BOTH'
    'CACHE_ENABLED': True,
    'CACHE_TIMEOUT': 3600,
    'USER_MODEL': settings.AUTH_USER_MODEL,
    'DEFAULT_ROLES': [
        {'name': 'Administrator', 'description': 'Full system access'},
        {'name': 'Editor', 'description': 'Can edit content but not manage users'},
        {'name': 'Viewer', 'description': 'Read-only access'},
    ],
    # Map codename -> human-readable label to override the library defaults.
    # Applied automatically after every `manage.py migrate`.
    # Example:
    #   PERMISSIONS_MANAGER_PERMISSION_LABELS = {
    #       "change_role": "Can modify role name and permissions",
    #       "assign_role": "Can assign roles to users",
    #   }
    'PERMISSION_LABELS': {},

    # Enable audit logging for RoleModel and UserRoleModel.
    # Requires `django-auditlog` to be installed and 'auditlog' in INSTALLED_APPS.
    # Default: False (opt-in).
    # To enable, add to your project settings:
    #   PERMISSIONS_MANAGER_AUDIT_LOG = True
    'AUDIT_LOG': False,
}

class AppSettings:
    """Helper class to access library settings with project-level overrides."""
    
    def __init__(self, prefix='PERMISSIONS_MANAGER_'):
        self.prefix = prefix

    def __getattr__(self, name):
        if name not in DEFAULTS:
            raise AttributeError(f"Setting {name} not found in defaults.")
            
        full_name = f"{self.prefix}{name}"
        return getattr(settings, full_name, DEFAULTS[name])

# Global instance for easy access
app_settings = AppSettings()
