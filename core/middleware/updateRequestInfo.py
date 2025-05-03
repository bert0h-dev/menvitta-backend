import logging
import threading

from django.utils.timezone import now

from core.base.responses import APIRequestInfo

logger = logging.getLogger(__name__)
_user_request_local = threading.local()

class UpdateUserInfoMiddleware:
  """
  Middleware que actualiza last_activity y last_ip del usuario autenticado en cada request a /api/.
  """

  def __init__(self, get_response):
    self.get_response = get_response
  
  def __call__(self, request):
    response = self.get_response(request)

    # Ignora rutas que no son API
    if not request.path.startswith('/api/'):
      return response
    
    try:
      if request.user.is_authenticated:
        user = request.user
        ip = APIRequestInfo.GetIPClient(request)
        update_fields = []

        # Actualiza la última actividade del usuario
        user.last_activity = now()
        update_fields.append('last_activity')

        if ip and ip != user.last_ip:
          user.last_ip = ip
          update_fields.append('last_ip')
        
        if update_fields:
          user.save(update_fields=update_fields)
    except Exception as e:
      logger.warning(f"[Middleware] No se pudo actualizar la informacion default del usuario: {e}")
    
    return response

def get_current_user():
  """
  Devuelve el usuario autenticado almacenado en el thread-local actual, o None si no hay usuario.
  """

  return getattr(_user_request_local, 'current_user', None)

class ThreadLocalUserMiddleware:
  """
  Middleware que almacena el usuario autenticado en una variable thread-local accesible globalmente
  durante el ciclo de vida de la request. Limpia el valor después de procesar la request.
  """

  def __init__(self, get_response):
    self.get_response = get_response
  
  def __call__(self, request):
    # Almacena el usuario autenticado en el thread-local
    _user_request_local.current_user = request.user if request.user.is_authenticated else None
    try:
      response = self.get_response(request)
    finally:
      # Limpia el thread-local para evitar fugas de memoria en servidores multihilo
      _user_request_local.current_user = None
    return response