import logging
import inspect

from functools import wraps
from typing import Callable, Any, Optional, Dict

from rest_framework import status

from django.db import transaction

from core.models import AccessLog
from core.base.responses import APIRequestInfo

logger = logging.getLogger(__name__)

def LogActionView(
  action_base: Optional[str] = None, 
  object_getter: Optional[Callable[[Any, Any, Dict, Any], str]] = None, 
  meta_getter: Optional[Callable[[Any, Any, Dict, Any], Dict]] = None
):
  """
  Decorador avanzado para registrar acciones con trazabilidad extendida.
  Aísla por completo la versión sync y async para evitar errores de 'await'.

  Params:
    - action_base: Texto base para la acción (opcional; usa la clase de la vista si no se provee).
    - object_getter: Función(view, request, kwargs, instance) -> str con descripción dinámica del objeto.
    - meta_getter:  Función(view, request, kwargs, instance) -> dict con 'object_id' y 'object_type'.
  """

  def decorator(view_func):
    if inspect.iscoroutinefunction(view_func):
      async def wrapped_async(self, request, *args, **kwargs):
        instance = None
        exception = None
        try:
          response = await view_func(self, request, *args, **kwargs)
          instance = getattr(response, 'instance', None)
          if instance is None and isinstance(response, dict):
            instance = response.get('log_instance')
          status_code = getattr(response, 'status_code', status.HTTP_200_OK)
        except Exception as e:
          response = None
          exception = e
          status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
        
        _schedule_log(self, request, response, status_code, action_base, object_getter, meta_getter, kwargs, exception, instance)

        if exception:
          raise exception
        return response
      
      return wraps(view_func)(wrapped_async)
    else:
      def wrapped_sync(self, request, *args, **kwargs):
        instance = None
        exception = None
        try:
          response = view_func(self, request, *args, **kwargs)
          instance = getattr(response, 'instance', None)
          if instance is None and isinstance(response, dict):
            instance = response.get('log_instance')
          status_code = getattr(response, 'status_code', status.HTTP_200_OK)
        except Exception as e:
          response = None
          exception = e
          status_code = status.HTTP_500_INTERNAL_SERVER_ERROR

        _schedule_log(self, request, response, status_code, action_base, object_getter, meta_getter, kwargs, exception, instance)

        if exception:
          raise exception
        return response
      
      return wraps(view_func)(wrapped_sync)
  return decorator

def _schedule_log(
  view: Any, 
  request: Any, 
  response: Any, 
  status_code: int, 
  action_base: Optional[str], 
  object_getter: Optional[Callable], 
  meta_getter: Optional[Callable], 
  view_kwargs: Dict, 
  exception: Optional[Exception] = None, 
  instance: Any = None
):
  """
  Función interna para crear el registro en AccessLog tras la respuesta o excepción.
  """
  
  try:
    user = request.user if getattr(request, 'user', None) and request.user.is_authenticated else None
    method = request.method
    path = request.get_full_path()
    ip = APIRequestInfo.GetIPClient(request)
    user_agent = request.META.get('HTTP_USER_AGENT', '')[:255]

    # Mensaje: Excepcion o bien el mensaje del payload
    if exception:
      message = str(exception)
    elif hasattr(response, 'data') and isinstance(response.data, dict):
      message = response.data.get('message', '')
    else:
      message = ''

    # Construye acción dinámica
    dynamic = ""
    if object_getter:
      try:
        dynamic = f": {object_getter(view, request, view_kwargs, instance)}"
      except Exception as e:
        logger.warning(f"[AccessLog Warning] object_getter failed: {e}")
        dynamic = ": (Error al obtener descripción)"
    
    action = f'{action_base or view.__class__.__name__}{dynamic}'

    # Obtiene metadatos si los hay
    meta = {}
    if meta_getter:
      try:
        meta = meta_getter(view, request, view_kwargs, instance) or {}
      except Exception as e:
        logger.warning(f"[AccessLog Warning] meta_getter failed: {e}")
        meta = {}
    
    def create_log():
      AccessLog.objects.create(
        user=user,
        method=method,
        path=path,
        action=action,
        status_code=status_code,
        message=message,
        ip_address=ip,
        user_agent=user_agent,
        object_id=meta.get('object_id'),
        object_type=meta.get('object_type'),
      )
    
    transaction.on_commit(create_log)

  except Exception as e:
    logger.error(f"[AccessLog Error] No se pudo registrar el log: {e}")