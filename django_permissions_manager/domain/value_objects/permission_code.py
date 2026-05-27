from dataclasses import dataclass

@dataclass(frozen=True)
class PermissionCode:
    """Value object representing a permission code in 'app_label.codename' format."""
    value: str

    def __post_init__(self):
        if '.' not in self.value or len(self.value.split('.')) != 2:
            raise ValueError(
                f"Invalid permission code '{self.value}'. "
                "Expected format: 'app_label.codename'."
            )
        app_label, codename = self.value.split('.')
        if not app_label or not codename:
            raise ValueError(
                f"Invalid permission code '{self.value}'. "
                "Both app_label and codename must be non-empty."
            )
