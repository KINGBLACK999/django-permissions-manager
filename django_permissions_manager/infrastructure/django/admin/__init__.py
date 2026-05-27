from django.contrib import admin
from ..models.role_model import RoleModel
from ..models.user_role_model import UserRoleModel
from ..models.permission_group_model import PermissionGroupModel

@admin.register(RoleModel)
class RoleAdmin(admin.ModelAdmin):
    list_display = ('name', 'entity_type', 'entity_id', 'is_active', 'is_system_role', 'created_at')
    list_filter = ('is_active', 'is_system_role', 'entity_type')
    search_fields = ('name', 'entity_id')
    filter_horizontal = ('permissions',)

@admin.register(UserRoleModel)
class UserRoleAdmin(admin.ModelAdmin):
    list_display = ('user', 'role', 'assigned_at', 'assigned_by')
    list_filter = ('role', 'assigned_at')
    search_fields = ('user__username', 'role__name')

@admin.register(PermissionGroupModel)
class PermissionGroupAdmin(admin.ModelAdmin):
    list_display = ('name', 'description')
    filter_horizontal = ('permissions',)
