from django.utils.translation import gettext_lazy as _

MSG_ERRORS = {
  # Authentication
  'invalid_credentials': _("Invalid credentials."), # Credenciales inválidas.
  'account_disabled': _("This account is disabled."), # Esta cuenta está desactivada.
  'token_required': _("Token is required."), # El token es requerido.
  'token_invalid': _("The token is invalid or has already been revoked."), # El token es inválido o ya ha sido cerrado.
  # Users
  'user_do_not_exists': _("User not found."), # Usuario no encontrado.
  'invalid_current_password': _("Current password is incorrect."), # La contraseña actual es incorrecta.
  'passwords_do_not_match': _("Passwords do not match."), # Las contraseñas no coinciden.
  'password_do_short': _("Password must be at least 8 characters long."), # La contraseña debe tener al menos 8 caracteres.
  'password_any_uppercase': _("Password must contain at least one uppercase letter."), # La contraseña debe contener al menos una letra mayúscula.
  'password_any_lowercase': _("Password must contain at least one lowercase letter."), # La contraseña debe contener al menos una letra minúscula.
  'password_any_number': _("Password must contain at least one number."), # La contraseña debe contener al menos un número.
  'password_any_special': _("Password must contain at least one special character (e.g. !@#$%)."), # La contraseña debe contener al menos un carácter especial (!@#$% etc).
  'invalid_language': _("Selected language is not supported."), # El idioma seleccionado no es compatible.
  'language_do_not_permisions': _("You do not have permission to change the language of this user."), # No tienes permiso para cambiar el idioma de este usuario.
  # Roles
  'role_do_exists': _("A role with this name already exists."), # Ya existe un rol con este nombre.
  'role_do_not_permisions': _("Must be a list of permission IDs."), # Debe ser una lista de IDs de permisos.
  'role_do_assign': _("Cannot delete a role that has users assigned."), # No se puede eliminar un rol que tiene usuarios asignados.
  # Permissions
  'permission_do_not_exists': _("Must provide a list of permission IDs."), # Debe enviar una lista de IDs de permisos.
}

MSG_SUCCESS = {
  # Authentication
  'login': _("Login successful."), # Inicio de sesión exitoso.
  'logout': _("Logout successful."), # Cierre de sesión exitoso.
  'token_refresh': _("Token refreshed successfully."), # Token actualizado exitosamente.
  # Users
  'user_list': _("User list."), # Lista de usuarios.
  'user_details': _("User details."), # Detalles del usuario.
  'user_create': _("User created successfully."), # Usuario creado exitosamente.
  'user_update': _("User updated successfully."), # Usuario actualizado exitosamente.
  'user_password_update': _("Password updated successfully."), # Contraseña cambiada exitosamente.
  'user_destroy': _("User deleted successfully."), # Usuario eliminado exitosamente.
  'user_update_language': _("User language updated successfully."), # Idioma del usuario actualizado exitosamente.
  # Roles
  'role_list': _("Role list."), # Lista de roles.
  'role_details': _("Role details."), # Detalles del rol.
  'role_create': _("Role created successfully."), # Rol creado exitosamente.
  'role_update': _("Role updated successfully."), # Rol actualizado exitosamente.
  'role_destroy': _("Role deleted successfully."), # Rol eliminado exitosamente.
  'role_assign': _("Role assigned successfully."), # Rol asignado exitosamente.
  # Permissions
  'permission_assign': _("Permission assigned successfully."), # Permiso asignado exitosamente.
  # Logs
  'log_list': _("Access logs list."), # Listado de logs de acceso.
  'log_details': _("Access log details."), # Detalle del log de acceso.
}

MSG_LOGS = {
  # Authentication
  'login': _("User logged in."), # Inicio de sesión.
  'logout': _("User logged out."), # Cierre de sesión.
  'token_refresh': _("Token refreshed."), # Actualización de token.
  # Users
  'user_list': _("Viewed user list."), # Visualizó el listado de usuarios.
  'user_details': _("Viewed user details."), # Visualizó los detalles del usuario.
  'user_create': _("Created a new user."), # Creó un nuevo usuario.
  'user_update': _("Updated user."), # Actualizó el usuario.
  'user_password_update': _("Updated user's password."), # Actualizó la contraseña del usuario.
  'user_destroy': _("Deleted user."), # Eliminó el usuario.
  'user_update_language': _("Updated user language."), # Actualizó idioma del usuario.
  # Roles
  'role_list': _("Viewed role list."), # Visualizó el listado de roles.
  'role_details': _("Viewed role details."), # Visualizó el detalle del rol.
  'role_create': _("Created a new role."), # Creó un nuevo rol.
  'role_update': _("Updated role."), # Actualizó el rol.
  'role_destroy': _("Deleted role."), # Eliminó el rol.
  'role_assign': _("Assigned role."), # Rol asignado.
  # Permissions
  'permission_assign': _("Assigned permission."), # Permiso asignado.
  # Logs
  'log_list': _("Viewed access logs list."), # Visualizó el listado de logs
  'log_details': _("Viewed access log details."), # Visualizó los detalles del log
  'log_export': _("Access logs list with export."), # Listado de logs de acceso con exportación.
}