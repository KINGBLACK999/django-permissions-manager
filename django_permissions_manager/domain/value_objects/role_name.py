from dataclasses import dataclass

MAX_ROLE_NAME_LENGTH = 255

@dataclass(frozen=True)
class RoleName:
    """Value object representing a role name."""
    value: str

    def __post_init__(self):
        if not self.value or not self.value.strip():
            raise ValueError("Role name cannot be empty.")
        if len(self.value) > MAX_ROLE_NAME_LENGTH:
            raise ValueError(
                f"Role name cannot exceed {MAX_ROLE_NAME_LENGTH} characters."
            )
