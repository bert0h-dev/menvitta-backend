from rest_framework import status
from rest_framework.response import Response
from rest_framework.request import Request

from typing import Any, Optional

def response_structure(success: bool = True, message: str = "Operacón exitosa.", data: Optional[Any] = None, errors: Optional[Any] = None, status_code: int = status.HTTP_200_OK) -> Response:
  return Response(
    {
      "success": success,
      "message": message,
      "status_code": status_code,
      "data": data,
      "errors": errors,
    },
    status=status_code
  )

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