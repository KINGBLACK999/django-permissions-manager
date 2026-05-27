import abc
from typing import List, Optional
from ..entities.role import Role
from ..value_objects.entity_reference import EntityReference

class RoleRepository(abc.ABC):
    """Abstract interface (Port) for Role persistence."""
    
    @abc.abstractmethod
    def save(self, role: Role) -> None:
        """Saves a role entity."""
        pass

    @abc.abstractmethod
    def get_by_id(self, role_id: str) -> Optional[Role]:
        """Retrieves a role by its unique ID."""
        pass

    @abc.abstractmethod
    def get_by_name(self, name: str, entity_reference: Optional[EntityReference] = None) -> Optional[Role]:
        """Retrieves a role by name within a specific scope."""
        pass

    @abc.abstractmethod
    def get_all(self) -> List[Role]:
        """Retrieves all roles."""
        pass

    @abc.abstractmethod
    def get_by_entity(self, entity_type: str, entity_id: str) -> List[Role]:
        """Retrieves all roles scoped to a specific entity."""
        pass

    @abc.abstractmethod
    def delete(self, role_id: str) -> None:
        """Deletes a role by ID."""
        pass
