class RoleException(Exception):
    """Base exception for role related errors."""
    pass

class RoleNotFoundException(RoleException):
    """Raised when a role is not found."""
    pass

class RoleAlreadyExistsException(RoleException):
    """Raised when a role with the same name already exists."""
    pass

class SystemRoleDeletionException(RoleException):
    """Raised when attempting to delete a system role."""
    pass
