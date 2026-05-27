from typing import List, Dict
from ...domain.services.role_factory import RoleFactory
from ...domain.repositories.role_repository import RoleRepository

class CreateDefaultRolesUseCase:
    """Application use case for initializing default system roles."""

    def __init__(self, role_repository: RoleRepository):
        """Initializes the use case.

        Args:
            role_repository: The role repository.
        """
        self.role_repository = role_repository

    def execute(self, default_roles: List[Dict[str, str]]) -> None:
        """Creates default system roles if they do not exist.

        Args:
            default_roles: A list of dictionaries containing 'name' and 'description'.
        """
        for role_data in default_roles:
            name = role_data['name']
            # Check if a global role with that name already exists
            if not self.role_repository.get_by_name(name, None):
                role = RoleFactory.create_role(
                    name=name,
                    description=role_data.get('description', ''),
                    is_system_role=True
                )
                self.role_repository.save(role)
