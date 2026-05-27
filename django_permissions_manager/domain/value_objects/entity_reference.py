from dataclasses import dataclass

@dataclass(frozen=True)
class EntityReference:
    """Value object representing a reference to an external entity."""
    entity_type: str
    entity_id: str

    def __post_init__(self):
        if not self.entity_type or not self.entity_type.strip():
            raise ValueError("EntityReference entity_type cannot be empty.")
        if not self.entity_id or not self.entity_id.strip():
            raise ValueError("EntityReference entity_id cannot be empty.")
