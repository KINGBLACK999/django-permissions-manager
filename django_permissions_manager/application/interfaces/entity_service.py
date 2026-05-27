import abc
from typing import Optional
from ..dto.entity_dto import EntityDTO

class EntityService(abc.ABC):
    """Abstract interface (Port) for interacting with external entities.

    Allows the permissions manager to validate or fetch information about 
    entities it doesn't own (e.g., Companies, Organizations).
    """
    @abc.abstractmethod
    def exists(self, entity_type: str, entity_id: str) -> bool:
        """Verifies if an external entity exists in the system."""
        pass

    @abc.abstractmethod
    def get_entity_details(self, entity_type: str, entity_id: str) -> Optional[EntityDTO]:
        """Fetches details of an external entity."""
        pass
