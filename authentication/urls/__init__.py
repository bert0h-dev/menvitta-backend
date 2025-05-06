from django.urls import include, path

urlpatterns = [
  path('auth/', include('authentication.urls.auth_urls')),
]