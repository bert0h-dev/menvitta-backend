from rest_framework import status

from typing import Any, Optional

from core.base.responses import response_structure
from core.utils.decorators import LogActionView

class APIResponseMixin:
  """
  Mixin que reemplaza `Response()` por `response_structure()` con formato estándar.
  Para usarlo, llama `self.success_response()` o `self.error_response()`.
  """

  def onlystatus_response(self, status_code: int = status.HTTP_204_NO_CONTENT) -> response_structure:
    """
    Retorna una respuesta JSON solo con el codigo del estatus.
    """

    return response_structure(
      status_code=status_code
    )

  def success_response(self, data: Optional[Any] = None, message: str = "Operación exitosa.", status_code: int = status.HTTP_200_OK) -> response_structure:
    """
    Retorna una respuesta JSON estándar para éxito.
    """

    return response_structure(
      success=True,
      message=message,
      data=data,
      errors=None,
      status_code=status_code
    )

  def error_response(self, message: str = "Error en la solicitud.", errors: Optional[Any] = None, status_code: int = status.HTTP_400_BAD_REQUEST) -> response_structure:
    """
    Retorna una respuesta JSON estándar para errores.
    """

    return response_structure(
      success=False,
      message=message,
      data=None,
      errors=errors,
      status_code=status_code
    )