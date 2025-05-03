from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.translation import gettext_lazy as _

from .models import User

@admin.register(User)
class UserAdmin(BaseUserAdmin):
  fieldsets = (
    (None, {'fields': ('email', 'password')}),
    (_('Personal info'), {'fields': ('first_name', 'last_name', 'username', 'user_type')}),
    (_('Preferences'), {'fields': ('language', 'timezone')}),
    (_('Security'), {'fields': ('password_changed', 'last_ip')}),
    (_('Permissions'), {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
    (_('Important dates'), {'fields': ('last_login', 'date_joined', 'last_activity')}),
  )
  add_fieldsets = (
    (None, {
      'classes': ('wide',),
      'fields': ('email', 'first_name', 'last_name', 'password1', 'password2', 'user_type', 'language', 'timezone', 'is_staff', 'is_active'),
    }),
  )
  list_display = ('email', 'username', 'first_name', 'last_name', 'user_type', 'is_staff', 'is_active')
  list_filter = ('is_staff', 'is_active', 'user_type', 'language')
  search_fields = ('email', 'first_name', 'last_name', 'username')
  ordering = ('-date_joined',)