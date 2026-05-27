from typing import List, Optional
from ..dto.role_dto import RoleDTO
from ..interfaces.entity_service import EntityService
from ...domain.services.role_factory import RoleFactory
from ...domain.services.role_manager import RoleManager
from ...domain.repositories.role_repository import RoleRepository
from ...domain.repositories.permission_repository import PermissionRepository
from ...domain.value_objects.entity_reference import EntityReference
from ...domain.value_objects.permission_code import PermissionCode

class CreateRoleUseCase:
    """Application use case for creating a new Role.

    This use case orchestrates the creation of a role, ensuring name uniqueness
    within the specified scope and resolving associated permissions.

    Attributes:
        role_repository (RoleRepository): Repository for role persistence.
        permission_repository (PermissionRepository): Repository to fetch permission entities.
        role_manager (RoleManager): Domain service to enforce business rules.
    """
    #: Valid operating modes.
    VALID_MODES = ('GLOBAL', 'ENTITY', 'BOTH')

    def __init__(
        self,
        role_repository: RoleRepository,
        permission_repository: PermissionRepository,
        role_manager: RoleManager,
        entity_service: Optional[EntityService] = None,
        mode: str = 'BOTH',
    ):
        """Initializes the use case with necessary collaborators.

        Args:
            role_repository: Repository for roles.
            permission_repository: Repository for permissions.
            role_manager: Manager for role business logic.
            entity_service: Optional service to validate external entities for scoped roles.
            mode: Operating mode ('GLOBAL', 'ENTITY', or 'BOTH'). Controls whether
                  global-only, entity-scoped-only, or both kinds of roles are allowed.
        """
        if mode not in self.VALID_MODES:
            raise ValueError(
                f"Invalid mode '{mode}'. Must be one of: {', '.join(self.VALID_MODES)}."
            )
        self.role_repository = role_repository
        self.permission_repository = permission_repository
        self.role_manager = role_manager
        self.entity_service = entity_service
        self.mode = mode

    def execute(
        self,
        name: str,
        description: str = "",
        entity_type: Optional[str] = None,
        entity_id: Optional[str] = None,
        permission_codes: Optional[List[str]] = None,
        is_system_role: bool = False
    ) -> RoleDTO:
        """Executes the role creation process.

        Args:
            name: The display name of the role.
            description: A brief description of the role's purpose.
            entity_type: The type of entity if scoped (e.g., 'Company').
            entity_id: The ID of the entity if scoped.
            permission_codes: List of strings representing permission codes to assign.
            is_system_role: Whether this is an immutable system-level role.

        Returns:
            RoleDTO: A data transfer object representing the created role.

        Raises:
            RoleAlreadyExistsException: If the name is already taken in the given scope.
        """
        # Enforce operating mode
        is_scoped = bool(entity_type and entity_id)
        if self.mode == 'GLOBAL' and is_scoped:
            raise ValueError(
                "Cannot create an entity-scoped role: the library is configured in GLOBAL mode."
            )
        if self.mode == 'ENTITY' and not is_scoped:
            raise ValueError(
                "Must provide both entity_type and entity_id: "
                "the library is configured in ENTITY mode."
            )

        entity_ref = None
        if entity_type and entity_id:
            entity_ref = EntityReference(entity_type, entity_id)
            if self.entity_service and not self.entity_service.exists(entity_type, entity_id):
                raise ValueError(
                    f"Entity '{entity_type}:{entity_id}' does not exist."
                )

        # 1. Validar regla de unicidad en el dominio
        self.role_manager.ensure_role_name_is_unique(name, entity_ref)

        # 2. Resolver permisos
        permissions = []
        if permission_codes:
            for code in permission_codes:
                permission = self.permission_repository.get_by_code(PermissionCode(code))
                if permission:
                    permissions.append(permission)

        # 3. Crear entidad de dominio usando la factoría
        role = RoleFactory.create_role(
            name=name,
            description=description,
            entity_reference=entity_ref,
            permissions=permissions,
            is_system_role=is_system_role
        )

        # 4. Persistir a través del repositorio
        self.role_repository.save(role)

        # 5. Mapear a DTO de salida
        return RoleDTO(
            id=role.id,
            name=role.name.value,
            description=role.description,
            entity_type=role.entity_reference.entity_type if role.entity_reference else None,
            entity_id=role.entity_reference.entity_id if role.entity_reference else None,
            permissions=[p.code.value for p in role.permissions],
            is_active=role.is_active,
            is_system_role=role.is_system_role,
            created_at=role.created_at,
            updated_at=role.updated_at
        )
