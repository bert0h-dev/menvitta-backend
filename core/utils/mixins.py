from core.base.responses import APIResponse
from core.utils.decorators import LogActionView

class ListOnlyMixin:
  """
  Mixin reutilizable para ViewSets DRF que provee el método 'list' con logging y respuesta uniforme.
  Cada ViewSet debe definir:
    - log_list_action: string para el log de la acción.
    - success_list: mensaje de éxito para la respuesta.
  """

  log_list_action = None # Ejemplo: "Listado de usuarios"
  message_list = None    # Ejemplo: "Usuarios listados correctamente"

  @LogActionView(lambda self, request, kwargs: self.log_list_action)
  def list(self, request, *args, **kwargs):
    if self.success_list is None:
      raise NotImplementedError("Debes definir 'success_list' en tu ViewSet.")
    
    queryset = super().filter_queryset(self.get_queryset())
    page = self.paginate_queryset(queryset)
    if page is not None:
      serializer = self.get_serializer(page, many=True)
      return APIResponse.success(
        data=self.get_paginated_response(serializer.data).data, 
        message=self.message_list
      )
      
    serializer = self.get_serializer(queryset, many=True)
    return APIResponse.success(
      data=serializer.data, 
      message=self.message_list
    )