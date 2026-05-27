import abc
from typing import List, Optional
from ..entities.permission_group import PermissionGroup

class PermissionGroupRepository(abc.ABC):
    @abc.abstractmethod
    def save(self, group: PermissionGroup) -> None:
        pass

    @abc.abstractmethod
    def get_by_id(self, group_id: str) -> Optional[PermissionGroup]:
        pass

    @abc.abstractmethod
    def get_by_name(self, name: str) -> Optional[PermissionGroup]:
        pass

    @abc.abstractmethod
    def get_all(self) -> List[PermissionGroup]:
        pass

    @abc.abstractmethod
    def delete(self, group_id: str) -> None:
        pass
