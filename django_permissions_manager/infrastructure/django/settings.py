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
