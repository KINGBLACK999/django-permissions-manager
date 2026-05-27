from dataclasses import dataclass

@dataclass(frozen=True)
class PermissionDTO:
    """Data Transfer Object for Permission data."""
    id: str
    code: str
    name: str
    content_type: str
