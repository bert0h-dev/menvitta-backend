import logging

from rest_framework.views import exception_handler
from rest_framework.exceptions import (
    NotAuthenticated, AuthenticationFailed, PermissionDenied,
    NotFound, MethodNotAllowed, Throttled, ValidationError
)

from core.base.responses import response_structure

logger = logging.getLogger(__name__)

def custom_exception_handler(exc, context):
  """
  Manejo global de exceptiones para formater con un response_structure
  """

  response = exception_handler(exc, context)

  if response is not None:
    status_code = response.status_code

    # Mensajes personalizados según el tipo de excepción
    exception_messages = {
      NotAuthenticated: "Debes iniciar sesión para acceder a este recurso.",
      AuthenticationFailed: "Correo o contraseña incorrectos.",
      PermissionDenied: "No tienes permiso para realizar esta acción.",
      NotFound: "El recurso solicitado no existe.",
      MethodNotAllowed: "Método HTTP no permitido para esta ruta.",
      Throttled: "Has enviado demasiadas solicitudes. Intenta más tarde.",
      ValidationError: "Hay errores en los datos enviados."
    }

    # Usa el mensaje por tipo de error o uno por defecto
    message = exception_messages.get(type(exc), "Ha ocurrido un error inesperado.")
    errors = response.data

    # Casos especiales para errores sin objetos
    if isinstance(errors, list):
      errors = {"non_field_errors": errors}
    
    return response_structure(
      success=False,
      message=message,
      errors=errors,
      status_code=status_code
    )

  # Para excepciones no manejadas, logueamos y retornamos 500
  logger.error("Excepción no controlada", exc_info=exc)
  return response_structure(
    success=False,
    message="Error interno del servidor.",
    errors={"server": ["Ocurrió un error inesperado. Intenta más tarde."]},
    status_code=500
  )