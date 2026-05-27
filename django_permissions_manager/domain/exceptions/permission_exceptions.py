class PermissionException(Exception):
    """Base exception for permission related errors."""
    pass

class PermissionNotFoundException(PermissionException):
    """Raised when a permission is not found."""
    pass
