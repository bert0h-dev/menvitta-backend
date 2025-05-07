from django.urls import path, include

from accounts.views.permissions_views import PermissionView, PermissionNameView

urlpatterns = [
    path('', PermissionView.as_view(), name='permissions-list'),
    path('name/', PermissionNameView.as_view(), name='permissions-names'),
]