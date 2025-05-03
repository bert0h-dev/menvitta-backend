from rest_framework import status
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet

from drf_spectacular.utils import extend_schema, extend_schema_view, OpenApiParameter
from django.shortcuts import get_object_or_404
from django.contrib.auth import get_user_model
from django_filters.rest_framework import DjangoFilterBackend

from core.base.messages import MSG_LOGS, MSG_SUCCESS, MSG_ERRORS
from core.base.responses import APIResponse
from core.base.common import GetModelName
from core.utils.mixins import ListOnlyMixin
from core.utils.permissions import IsAdmin, IsStaff, IsUserAuthenticated
from core.utils.decorators import LogActionView

from accounts.filters import UserFilter
from accounts.serializers.users_serializer import UserSerializer, ChangePasswordSerializer, ChangeUserLanguageSerializer

User = get_user_model()

@extend_schema_view(
  list=extend_schema(
    summary="Listar usuarios del sistema",
    description="Permite listar usuarios del sistema. Solo accesible a administradores o staff.",
  ),
  create=extend_schema(
    summary="Crear un nuevo usuario",
    description="Permite crear usuarios en el sistema. Solo accesible a administradores o staff.",
  ),
  retrieve=extend_schema(
    summary="Detalle de un usuario",
    description="Permite ver el detalle de un usuario en espeficio. Solo accesible a administradores o staff.",
  ),
  update=extend_schema(
    summary="Actualización de la información de un usuario",
    description="Permite actualizar la información de un usuario en especifico. Solo accesible a administradores o staff.",
  ),
  partial_update=extend_schema(
    summary="Actualización de información parcial de un usuario",
    description="Permite actualizar la información de manera parcial de un usuario en especifico. Solo accesible a administradores o staff.",
  ),
  destroy=extend_schema(
    summary="Eliminar un usuario del sistema",
    description="Permite eliminar un usuario dentro del sistema. Solo accesible a administradores o staff.",
  )
)
class UserViewSet(ListOnlyMixin, ModelViewSet):
  queryset = User.objects.all()
  serializer_class = UserSerializer
  permission_classes = [IsAdmin, IsStaff]
  filter_backends = [DjangoFilterBackend]
  filterset_class = UserFilter

  # Configuracion de mixin
  log_list_action = MSG_LOGS["user_list"]
  message_list = MSG_SUCCESS["user_list"]

  def get_queryset(self):
    return User.objects.all()
  
  @LogActionView(
    action_base=MSG_LOGS["user_details"],
    object_getter=lambda self, request, kwargs, instance: instance.email,
    meta_getter=lambda view, request, view_kwargs, instance: {
      "object_id": instance.id,
      "object_type": GetModelName(instance),
    }
  )
  def retrieve(self, request, *args, **kwargs):
    instance = self.get_object()
    serializer = self.get_serializer(instance)
    return APIResponse.success(
      data=serializer.data, 
      message=MSG_SUCCESS["user_details"]
    )
  
  @LogActionView(
    action_base=MSG_LOGS["user_create"],
    object_getter=lambda self, request, kwargs, instance: instance.email,
    meta_getter=lambda view, request, view_kwargs, instance: {
      "object_id": instance.id,
      "object_type": GetModelName(instance),
    }
  )
  def create(self, request, *args, **kwargs):
    serializer = self.get_serializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    self.perform_create(serializer)
    return APIResponse.success(
      data=serializer.data, 
      message=MSG_SUCCESS["user_create"], 
      status_code=status.HTTP_201_CREATED
    )
  
  @LogActionView(
    action_base=MSG_LOGS["user_update"],
    object_getter=lambda self, request, kwargs, instance: instance.email,
    meta_getter=lambda view, request, view_kwargs, instance: {
      "object_id": instance.id,
      "object_type": GetModelName(instance),
    }
  )
  def update(self, request, *args, **kwargs):
    partial = kwargs.pop('partial', False)
    instance = self.get_object()
    serializer = self.get_serializer(instance, data=request.data, partial=partial)
    serializer.is_valid(raise_exception=True)
    self.perform_update(serializer)
    return APIResponse.success(
      data=serializer.data, 
      message=MSG_SUCCESS["user_update"]
    )
  
  @LogActionView(
    action_base=MSG_LOGS["user_update"],
    object_getter=lambda self, request, kwargs, instance: instance.email,
    meta_getter=lambda view, request, view_kwargs, instance: {
      "object_id": instance.id,
      "object_type": GetModelName(instance),
    }
  )
  def partial_update(self, request, *args, **kwargs):
      partial = True
      instance = self.get_object()
      serializer = self.get_serializer(instance, data=request.data, partial=partial)
      serializer.is_valid(raise_exception=True)
      self.perform_update(serializer)
      return APIResponse.success(
        data=serializer.data, 
        message=MSG_SUCCESS["user_update"]
      )

  @LogActionView(
    action_base=MSG_LOGS["user_destroy"]
  )
  def destroy(self, request, *args, **kwargs):
    instance = self.get_object()
    self.perform_destroy(instance)
    return APIResponse.success(
      message=MSG_SUCCESS["user_destroy"], 
      status_code=status.HTTP_204_NO_CONTENT
    )

class ChangePasswordView(APIView):
  permission_classes = [IsAdmin, IsStaff]

  @LogActionView(
    action_base=MSG_LOGS["user_password_update"],
    object_getter=lambda self, request, kwargs, instance: instance.email,
    meta_getter=lambda view, request, view_kwargs, instance: {
      "object_id": instance.id,
      "object_type": GetModelName(instance),
    }
  )
  def put(self, request, user_id, *args, **kwargs):
    # valida si el usuario existe si no regresa un 404
    target = get_object_or_404(User, pk=user_id)
    
    # Inyectamos el target en el serializer
    serializer = ChangePasswordSerializer(data=request.data, context={
      'request': request,
      'target_user': target
    })
    serializer.is_valid(raise_exception=True)

    # Guarda y arma el Response
    updated_user = serializer.save()
    resp = APIResponse.success(message=MSG_SUCCESS["user_password_update"])
    resp.instance = updated_user
    return resp

class ChangeUserLanguageView(APIView):
  permission_classes = [IsUserAuthenticated]

  @LogActionView(
    action_base=MSG_LOGS["user_update_language"],
    object_getter=lambda self, request, kwargs, instance: instance.email,
    meta_getter=lambda view, request, view_kwargs, instance: {
      "object_id": instance.id,
      "object_type": GetModelName(instance),
    }
  )
  def put(self, request, user_id, *args, **kwargs):
    # Valida si el usuario existe si no regresa un 404
    target_user = get_object_or_404(User, pk=user_id)

    # Solo el propio usuario puede cambiar el idioma
    if request.user != target_user:
      return APIResponse.error(
        message=MSG_ERRORS["language_do_not_permisions"], 
        status_code=status.HTTP_403_FORBIDDEN
      )

    # Valida payload
    serializer = ChangeUserLanguageSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)

    # Asigna y guarda
    target_user.language = serializer.validated_data["language"]
    target_user.save()

    # Arma el Response
    resp = APIResponse.success(
      data={"language": target_user.language}, 
      message=MSG_SUCCESS["user_update_language"]
    )
    resp.instance = target_user
    return resp