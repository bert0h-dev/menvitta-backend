from rest_framework.routers import DefaultRouter

from django.urls import path, include

from accounts.views.roles_views import RoleViewSet, AssignRoleToUserView, RemoveRoleToUserView

rRoles = DefaultRouter()
rRoles.register(r'roles', RoleViewSet, basename='rol')

urlpatterns = [
    path('', include(rRoles.urls)),
    path('assign/', AssignRoleToUserView.as_view(), name='assign-role-to-user'),
    path('remove/', RemoveRoleToUserView.as_view(), name='remove-role-to-user'),
]