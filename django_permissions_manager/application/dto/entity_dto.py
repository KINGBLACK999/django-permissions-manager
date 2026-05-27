from dataclasses import dataclass

@dataclass(frozen=True)
class EntityDTO:
    """Data Transfer Object for external Entity data."""
    entity_type: str
    entity_id: str
