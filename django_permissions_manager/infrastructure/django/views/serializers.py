from rest_framework import serializers


class RoleSerializer(serializers.Serializer):
    id = serializers.UUIDField(read_only=True)
    name = serializers.CharField(max_length=255)
    description = serializers.CharField(allow_blank=True, default="")
    entity_type = serializers.CharField(allow_null=True, required=False, default=None)
    entity_id = serializers.CharField(allow_null=True, required=False, default=None)
    permission_codes = serializers.ListField(
        child=serializers.CharField(), write_only=True, required=False, default=list
    )
    permissions = serializers.ListField(child=serializers.CharField(), read_only=True)
    is_active = serializers.BooleanField(read_only=True)
    is_system_role = serializers.BooleanField(read_only=True)
    created_at = serializers.DateTimeField(read_only=True)
    updated_at = serializers.DateTimeField(read_only=True)


class AssignRoleSerializer(serializers.Serializer):
    role_id = serializers.UUIDField()
    assigned_by_id = serializers.CharField(required=False, allow_null=True, default=None)


class UserRoleSerializer(serializers.Serializer):
    id = serializers.UUIDField(read_only=True)
    user_id = serializers.CharField(read_only=True)
    role_id = serializers.UUIDField(read_only=True)
    role_name = serializers.CharField(read_only=True)
    assigned_at = serializers.DateTimeField(read_only=True)
    assigned_by = serializers.CharField(read_only=True, allow_null=True)


class PermissionGroupSerializer(serializers.Serializer):
    id = serializers.UUIDField(read_only=True)
    name = serializers.CharField(max_length=255)
    description = serializers.CharField(allow_blank=True, default="")
    permission_codes = serializers.ListField(
        child=serializers.CharField(), write_only=True, required=False, default=list
    )
    permissions = serializers.ListField(child=serializers.CharField(), read_only=True)


class AssignGroupToRoleSerializer(serializers.Serializer):
    group_id = serializers.UUIDField()
