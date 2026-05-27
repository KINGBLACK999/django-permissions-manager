from .repositories.django_role_repository import DjangoRoleRepository
from .repositories.django_user_role_repository import DjangoUserRoleRepository
from .repositories.django_permission_repository import DjangoPermissionRepository
from .repositories.django_permission_group_repository import DjangoPermissionGroupRepository
from .settings import app_settings
from ...domain.services.role_manager import RoleManager
from ...domain.services.permission_checker import PermissionChecker
from ...application.use_cases.check_user_permission import CheckUserPermissionUseCase
from ...application.use_cases.create_role import CreateRoleUseCase
from ...application.use_cases.assign_role_to_user import AssignRoleToUserUseCase
from ...application.use_cases.remove_role_from_user import RemoveRoleFromUserUseCase
from ...application.use_cases.get_user_roles import GetUserRolesUseCase
from ...application.use_cases.create_permission_group import CreatePermissionGroupUseCase
from ...application.use_cases.assign_permission_group_to_role import AssignPermissionGroupToRoleUseCase


def get_check_permission_use_case() -> CheckUserPermissionUseCase:
    return CheckUserPermissionUseCase(
        user_role_repository=DjangoUserRoleRepository(),
        permission_checker=PermissionChecker(),
    )


def get_create_role_use_case() -> CreateRoleUseCase:
    role_repo = DjangoRoleRepository()
    return CreateRoleUseCase(
        role_repository=role_repo,
        permission_repository=DjangoPermissionRepository(),
        role_manager=RoleManager(role_repo),
        mode=app_settings.MODE,
    )


def get_assign_role_use_case() -> AssignRoleToUserUseCase:
    return AssignRoleToUserUseCase(
        user_role_repository=DjangoUserRoleRepository(),
        role_repository=DjangoRoleRepository(),
    )


def get_remove_role_use_case() -> RemoveRoleFromUserUseCase:
    return RemoveRoleFromUserUseCase(
        user_role_repository=DjangoUserRoleRepository(),
    )


def get_user_roles_use_case() -> GetUserRolesUseCase:
    return GetUserRolesUseCase(
        user_role_repository=DjangoUserRoleRepository(),
    )


def get_create_permission_group_use_case() -> CreatePermissionGroupUseCase:
    return CreatePermissionGroupUseCase(
        group_repository=DjangoPermissionGroupRepository(),
        permission_repository=DjangoPermissionRepository(),
    )


def get_assign_permission_group_to_role_use_case() -> AssignPermissionGroupToRoleUseCase:
    return AssignPermissionGroupToRoleUseCase(
        role_repository=DjangoRoleRepository(),
        group_repository=DjangoPermissionGroupRepository(),
    )
