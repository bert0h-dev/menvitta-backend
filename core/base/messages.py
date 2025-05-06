from django.utils.translation import gettext_lazy as _

MESSAGES = {
    "generic": {
        # Generic messages
        'bad_request': _("Validation errors."), # Errores de validación.
        'unauthorized': _("Not authorized. Invalid token."), # No autorizado. Token no válido.
        'forbidden': _('Access denied.'), # Acceso denegado.
        'not_found': _("Resource not found."), # Recurso no encontrado.
        'conflict': _("Conflict in processing the request."), # Conflicto al procesar la solicitud.
        'unprocessable': _("The entity cannot be processed."), # La entidad no puede ser procesada.
        'internal_server_error': _("Internal server error."), # Error interno del servidor.
    },
    "success": {
        # Authentication
        'login': _("Login successful."), # Inicio de sesión exitoso.
        'token_refresh': _("Token refreshed successfully."), # Token actualizado exitosamente.

        # User
        'user_list': _("User list."), # Lista de usuarios.
        'user_recovered': _("User successfully recovered."), # Usuario recuperado correctamente.
        'user_create': _("User created successfully."), # Usuario creado exitosamente.
        'user_update': _("User updated successfully."), # Usuario actualizado exitosamente.
        'user_password_update': _("Updated user password."), # Actualizó la contraseña del usuario.
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
    },
    "errors": {
        # Authentication
        'token_required': _("Token is required."), # El token es requerido.
        'token_invalid': _("The token is invalid or has already been revoked."), # El token es inválido o ya ha sido cerrado.
        'refresh_failed': _("Could not refresh the session."), # No se pudo actualizar la sesión.
        'logout_failed': _("Could not close the session."), # No se pudo cerrar la sesión.

        # Generics
        'field_required': _("Field is required."), # Este campo es requerido

        # Users
        'user_invalid_credentials': _("User not found, invalid credentials."), # Usuario no encontrado, credenciales inválidas.
        'user_invalid_email': _("A user with this email already exists."), # Ya existe un usuario con este email.
        'user_disabled': _("User is disabled."), # El usuario está desactivado. 
        'invalid_current_password': _("Current password is incorrect."), # La contraseña actual es incorrecta.
        'no_permission_to_modify_user': _("You do not have permission to change this user."), # No tienes permiso para modificar este usuario.
        'user_do_not_exists': _("User not found."), # Usuario no encontrado.
        'passwords_do_not_match': _("Passwords do not match."), # Las contraseñas no coinciden.
        'password_do_short': _("Password must be at least 8 characters long."), # La contraseña debe tener al menos 8 caracteres.
        'password_any_uppercase': _("Password must contain at least one uppercase letter."), # La contraseña debe contener al menos una letra mayúscula.
        'password_any_lowercase': _("Password must contain at least one lowercase letter."), # La contraseña debe contener al menos una letra minúscula.
        'password_any_number': _("Password must contain at least one number."), # La contraseña debe contener al menos un número.
        'password_any_special': _("Password must contain at least one special character (e.g. !@#$%)."), # La contraseña debe contener al menos un carácter especial (!@#$% etc)

        # Roles
        'role_do_exists': _("A role with this name already exists."), # Ya existe un rol con este nombre.
        'role_do_not_permissions': _("Must be a list of permission IDs."), # Debe ser una lista de IDs de permisos.
        'role_do_assign': _("Cannot delete a role that has users assigned."), # No se puede eliminar un rol que tiene usuarios asignados.

        # Permissions
        'permissions_list_required': _("Must provide a list of permission IDs."), # Debe enviar una lista de IDs de permisos.
    },
    "logs": {
        # Authentication
        'login': _("User logged in."), # Inicio de sesión.
        'logout': _("User logged out."), # Cierre de sesión.
        'token_refresh': _("Token refreshed."), # Actualización de token.
        # Users
        'user_list': _("Viewed user list."), # Visualizó el listado de usuarios.
        'user_details': _("Viewed user details."), # Visualizó los detalles del usuario.
        'user_create': _("Created a new user."), # Creó un nuevo usuario.
        'user_update': _("Updated user."), # Actualizó el usuario.
        'user_password_update': _("Password updated successfully."), # Contraseña cambiada exitosamente.
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
}

def get_message(category: str, key: str, default: str = None) -> str:
    """
    Recupera de forma segura un mensaje del diccionario MESSAGES.

    Args:
        category (str): La categoría principal (por ejemplo, "generic", "errors", "logs").
        key (str): La clave específica del mensaje dentro de la categoría.
        default (str, opcional): Mensaje por defecto si no se encuentra la clave. Si no se proporciona, retorna un mensaje de error estándar.

    Returns:
        str: El mensaje localizado.
    """
    try:
        return MESSAGES[category][key]
    except KeyError:
        if default is not None:
            return default
        # Mensaje de error si no se encuentra la clave
        return _("Message not found for category '%(category)s' and key '%(key)s'.") % {"category": category, "key": key}