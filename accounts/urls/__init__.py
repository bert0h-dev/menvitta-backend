from django.urls import include, path

urlpatterns = [
  path('users/', include('accounts.urls.users_urls')),
  path('roles/', include('accounts.urls.roles_urls')),
  path('permissions/', include('accounts.urls.permissions_urls')),
]