from rest_framework.permissions import BasePermission

class IsAdmin(BasePermission):
  """
  Permite acceso solo a usuarios administradores.
  """

  def has_permission(self, request, view):
    return bool(request.user and request.user.is_authenticated and getattr(request.user, 'user_type', None) == 'admin')

class IsStaff(BasePermission):
  """
  Permite acceso solo a usuarios staff.
  """

  def has_permission(self, request, view):
    return bool(request.user and request.user.is_authenticated and getattr(request.user, 'user_type', None) == 'staff')

class IsUserAuthenticated(BasePermission):
  """
  Permite acceso a los usuarios que esten autenticados
  """

  def has_permission(self, request, view):
    return bool(request.user and request.user.is_authenticated)