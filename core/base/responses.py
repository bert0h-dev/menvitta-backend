from typing import Any, Optional

from rest_framework import status
from rest_framework.response import Response
from rest_framework.request import Request

from django.conf import settings

class APIResponse:
  """
  Método utilitario para extraer info del request,
  como la IP del cliente.
  """

  version = getattr(settings, 'API_VERSION', '1.0.0') #Por si no esta definida

  @classmethod
  def success(cls, data: Optional[Any] = None, message: str = "Operación exitosa", status_code: int = status.HTTP_200_OK) -> Response:
    """
    Retorna una respuesta JSON estándar para éxito.
    """

    return Response({
      "success": True,
      "version": cls.version,
      "status": status_code,
      "message": message,
      "data": {} if data is None else data
    }, status=status_code)

  @classmethod
  def error(cls, message: str = "Error en la operación", errors: Optional[Any] = None, status_code: int = status.HTTP_400_BAD_REQUEST) -> Response:
    """
    Retorna una respuesta JSON estándar para errores.
    """

    return Response({
      "success": False,
      "version": cls.version,
      "status": status_code,
      "message": message,
      "errors": {} if errors is None else errors
    }, status=status_code)

class APIRequestInfo:
  @staticmethod
  def GetIPClient(request: Request) -> str:
    """
    Método utilitario para extraer info del request,
    como la IP del cliente.
    """

    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
      ip = x_forwarded_for.split(',')[0].strip()
    else:
      ip = request.META.get('REMOTE_ADDR')
    return ip