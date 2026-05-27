from rest_framework import status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet

from ..services import (
    get_assign_permission_group_to_role_use_case,
    get_assign_role_use_case,
    get_create_permission_group_use_case,
    get_create_role_use_case,
    get_remove_role_use_case,
    get_user_roles_use_case,
)
from ...django.repositories.django_role_repository import DjangoRoleRepository
from ...django.repositories.django_permission_group_repository import DjangoPermissionGroupRepository
from ....domain.services.role_manager import RoleManager
from .serializers import (
    AssignGroupToRoleSerializer,
    AssignRoleSerializer,
    PermissionGroupSerializer,
    RoleSerializer,
    UserRoleSerializer,
)


class RoleViewSet(ViewSet):
    """
    Manages roles: create, list, activate/deactivate, assign permissions groups.

    list:   GET  /roles/
    create: POST /roles/
    activate:   POST /roles/{id}/activate/
    deactivate: POST /roles/{id}/deactivate/
    assign_group: POST /roles/{id}/assign_group/
    """

    def list(self, request):
        roles = DjangoRoleRepository().get_all()
        data = [
            {
                'id': r.id,
                'name': r.name.value,
                'description': r.description,
                'entity_type': r.entity_reference.entity_type if r.entity_reference else None,
                'entity_id': r.entity_reference.entity_id if r.entity_reference else None,
                'permissions': [p.code.value for p in r.permissions],
                'is_active': r.is_active,
                'is_system_role': r.is_system_role,
                'created_at': r.created_at,
                'updated_at': r.updated_at,
            }
            for r in roles
        ]
        return Response(data)

    def create(self, request):
        serializer = RoleSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        d = serializer.validated_data
        try:
            use_case = get_create_role_use_case()
            dto = use_case.execute(
                name=d['name'],
                description=d.get('description', ''),
                entity_type=d.get('entity_type'),
                entity_id=d.get('entity_id'),
                permission_codes=d.get('permission_codes', []),
            )
        except ValueError as e:
            return Response({'detail': str(e)}, status=status.HTTP_400_BAD_REQUEST)
        return Response(RoleSerializer(dto).data, status=status.HTTP_201_CREATED)

    @action(detail=True, methods=['post'])
    def activate(self, request, pk=None):
        role_repo = DjangoRoleRepository()
        role = role_repo.get_by_id(pk)
        if not role:
            return Response({'detail': 'Role not found.'}, status=status.HTTP_404_NOT_FOUND)
        RoleManager(role_repo).activate_role(role)
        return Response({'detail': 'Role activated.'})

    @action(detail=True, methods=['post'])
    def deactivate(self, request, pk=None):
        role_repo = DjangoRoleRepository()
        role = role_repo.get_by_id(pk)
        if not role:
            return Response({'detail': 'Role not found.'}, status=status.HTTP_404_NOT_FOUND)
        try:
            RoleManager(role_repo).deactivate_role(role)
        except Exception as e:
            return Response({'detail': str(e)}, status=status.HTTP_400_BAD_REQUEST)
        return Response({'detail': 'Role deactivated.'})

    @action(detail=True, methods=['post'], url_path='assign_group')
    def assign_group(self, request, pk=None):
        serializer = AssignGroupToRoleSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            use_case = get_assign_permission_group_to_role_use_case()
            dto = use_case.execute(role_id=pk, group_id=str(serializer.validated_data['group_id']))
        except ValueError as e:
            return Response({'detail': str(e)}, status=status.HTTP_400_BAD_REQUEST)
        return Response(RoleSerializer(dto).data)


class UserRoleViewSet(ViewSet):
    """
    Manages user-role assignments.

    list:   GET  /users/{user_id}/roles/
    assign: POST /users/{user_id}/roles/
    remove: DELETE /users/{user_id}/roles/{id}/
    """

    def list(self, request, user_pk=None):
        use_case = get_user_roles_use_case()
        dtos = use_case.execute(user_id=user_pk)
        return Response(UserRoleSerializer(dtos, many=True).data)

    def create(self, request, user_pk=None):
        serializer = AssignRoleSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        d = serializer.validated_data
        try:
            use_case = get_assign_role_use_case()
            dto = use_case.execute(
                user_id=user_pk,
                role_id=str(d['role_id']),
                assigned_by_id=d.get('assigned_by_id'),
            )
        except ValueError as e:
            return Response({'detail': str(e)}, status=status.HTTP_400_BAD_REQUEST)
        return Response(UserRoleSerializer(dto).data, status=status.HTTP_201_CREATED)

    def destroy(self, request, user_pk=None, pk=None):
        try:
            get_remove_role_use_case().execute(user_role_id=pk)
        except ValueError as e:
            return Response({'detail': str(e)}, status=status.HTTP_404_NOT_FOUND)
        return Response(status=status.HTTP_204_NO_CONTENT)


class PermissionGroupViewSet(ViewSet):
    """
    Manages permission groups.

    list:   GET  /permission-groups/
    create: POST /permission-groups/
    """

    def list(self, request):
        groups = DjangoPermissionGroupRepository().get_all()
        data = [
            {
                'id': g.id,
                'name': g.name,
                'description': g.description,
                'permissions': [p.code.value for p in g.permissions],
            }
            for g in groups
        ]
        return Response(data)

    def create(self, request):
        serializer = PermissionGroupSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        d = serializer.validated_data
        try:
            use_case = get_create_permission_group_use_case()
            dto = use_case.execute(
                name=d['name'],
                description=d.get('description', ''),
                permission_codes=d.get('permission_codes', []),
            )
        except ValueError as e:
            return Response({'detail': str(e)}, status=status.HTTP_400_BAD_REQUEST)
        return Response(PermissionGroupSerializer(dto).data, status=status.HTTP_201_CREATED)
