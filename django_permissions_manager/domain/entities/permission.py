from dataclasses import dataclass
from ..value_objects.permission_code import PermissionCode

@dataclass
class Permission:
    """Domain entity representing a granular permission."""
    id: str
    code: PermissionCode
    name: str
    content_type: str

    def matches(self, code: str) -> bool:
        """Checks if the permission matches the given code string."""
        return self.code.value == code
