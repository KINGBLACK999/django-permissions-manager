from dataclasses import dataclass

@dataclass(frozen=True)
class UserId:
    """Value object representing a user identifier."""
    value: str

    def __post_init__(self):
        if not self.value or not str(self.value).strip():
            raise ValueError("UserId cannot be empty.")
