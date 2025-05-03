from rest_framework.routers import DefaultRouter

from django.urls import path, include

from accounts.views.users_views import UserViewSet, ChangePasswordView, ChangeUserLanguageView

rUsers = DefaultRouter()
rUsers.register(r'users', UserViewSet, basename='user')

urlpatterns = [
  path('', include(rUsers.urls)),
  path('<int:user_id>/change-password/', ChangePasswordView.as_view(), name='user_change_password'),
  path('<int:user_id>/language/', ChangeUserLanguageView.as_view(), name='user_change_language'),
]