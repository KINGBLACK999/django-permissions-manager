from django.urls import path, include
from rest_framework.routers import DefaultRouter, SimpleRouter

from .views.api import PermissionGroupViewSet, RoleViewSet, UserRoleViewSet

router = DefaultRouter()
router.register(r'roles', RoleViewSet, basename='role')
router.register(r'permission-groups', PermissionGroupViewSet, basename='permission-group')

user_roles_router = SimpleRouter()
user_roles_router.register(r'roles', UserRoleViewSet, basename='user-role')

urlpatterns = [
    path('', include(router.urls)),
    # /users/<user_pk>/roles/  and  /users/<user_pk>/roles/<pk>/
    path('users/<str:user_pk>/', include(user_roles_router.urls)),
]
