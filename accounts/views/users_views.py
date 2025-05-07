from rest_framework import status
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet

from drf_spectacular.utils import extend_schema, extend_schema_view, OpenApiExample
from django.shortcuts import get_object_or_404
from django.contrib.auth import get_user_model
from django_filters.rest_framework import DjangoFilterBackend

from core.base.messages import get_message
from core.base.common import GetModelName
from core.base.pagination import BasePagination
from core.base.serializers.responses_serializer import error_400_serializer, error_403_serializer
from core.throttle import SensitiveActionThrottle
from core.utils.mixins import APIResponseMixin
from core.utils.permissions import IsAdmin, IsStaff, IsUserAuthenticated
from core.utils.decorators import LogActionView

from accounts.filters import UserFilter
from accounts.serializers.users_serializer import UserSerializer, CustomCreateUserSerializer, ChangePasswordSerializer, ChangeUserLanguageSerializer

User = get_user_model()

@extend_schema_view(
  list=extend_schema(
    summary="Listar usuarios del sistema",
    description="Permite listar usuarios del sistema. Solo accesible a administradores o staff.",
    responses={
      200: UserSerializer
    }
  ),
  create=extend_schema(
    summary="Crear un nuevo usuario",
    description="Permite crear usuarios en el sistema. Solo accesible a administradores o staff.",
    responses={
      200: CustomCreateUserSerializer,
      400: error_400_serializer
    }
  ),
  retrieve=extend_schema(
    summary="Detalle de un usuario",
    description="Permite ver el detalle de un usuario en espeficio. Solo accesible a administradores o staff.",
  ),
  update=extend_schema(
    summary="Actualización de la información de un usuario",
    description="Permite actualizar la información de un usuario en especifico. Solo accesible a administradores o staff.",
    responses={
      200: UserSerializer,
      400: error_400_serializer
    }
  ),
  partial_update=extend_schema(
    summary="Actualización de información parcial de un usuario",
    description="Permite actualizar la información de manera parcial de un usuario en especifico. Solo accesible a administradores o staff.",
    responses={
      200: UserSerializer,
      400: error_400_serializer
    }
  ),
  destroy=extend_schema(
    summary="Eliminar un usuario del sistema",
    description="Permite eliminar un usuario dentro del sistema. Solo accesible a administradores o staff.",
    responses={
      204: OpenApiExample("Response", value={"status_code": "204"}, response_only=True, status_codes=["204"]),
    }
  )
)
class UserViewSet(APIResponseMixin, ModelViewSet):
  queryset = User.objects.all()
  permission_classes = [IsAdmin | IsStaff]
  pagination_class = BasePagination
  filter_backends = [DjangoFilterBackend]
  filterset_class = UserFilter

  def get_serializer_class(self):
    if self.action == 'create':
      return CustomCreateUserSerializer
    if self.action == 'partial_update':
      return UserSerializer
    return UserSerializer

  @LogActionView(action_base=get_message("logs", "user_list"))
  def list(self, request, *args, **kwargs): 
    queryset = self.filter_queryset(self.get_queryset())
    page = self.paginate_queryset(queryset)

    if page is not None:
      serializer = self.get_serializer(page, many=True)
      return self.success_response(
        data=self.get_paginated_response(serializer.data).data, 
        message=get_message("success", "user_list")
      )
      
    serializer = self.get_serializer(queryset, many=True)
    return self.success_response(
      data=serializer.data, 
      message=get_message("success", "user_list")
    )
  
  @LogActionView(
    action_base=get_message("logs", "user_details"),
    object_getter=lambda self, request, kwargs, instance: instance.email,
    meta_getter=lambda view, request, view_kwargs, instance: {
      "object_id": instance.id,
      "object_type": GetModelName(instance),
    }
  )
  def retrieve(self, request, *args, **kwargs):
    instance = self.get_object()
    serializer = self.get_serializer(instance)
    return self.success_response(
      data=serializer.data, 
      message=get_message("success", "user_recovered")
    )
  
  @LogActionView(
    action_base=get_message("logs", "user_create"),
    object_getter=lambda self, request, kwargs, instance: instance.email,
    meta_getter=lambda view, request, view_kwargs, instance: {
      "object_id": instance.id,
      "object_type": GetModelName(instance),
    }
  )
  def create(self, request, *args, **kwargs):
    serializer = self.get_serializer(data=request.data)
    if serializer.is_valid():
      serializer.save()
      return self.success_response(
        message=get_message("success", "user_create"), 
        status_code=status.HTTP_201_CREATED
      )
    
    return self.error_response(
      message=get_message("generic", "bad_request"),
      errors=serializer.errors,
      status_code=status.HTTP_400_BAD_REQUEST
    )

  @LogActionView(
    action_base=get_message("logs", "user_update"),
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
    if serializer.is_valid():
      self.perform_update(serializer)
      return self.success_response(
        data=serializer.data, 
        message=get_message("success", "user_update")
      )
    
    return self.error_response(
      message=get_message("generic", "bad_request"),
      errors=serializer.errors,
      status_code=status.HTTP_400_BAD_REQUEST
    )

  @LogActionView(action_base=get_message("logs", "user_destroy"))
  def destroy(self, request, *args, **kwargs):
    instance = self.get_object()
    self.perform_destroy(instance)
    return self.onlystatus_response(
      status_code=status.HTTP_204_NO_CONTENT
    )

@extend_schema(
  summary="Actualización de la contraseña de un usuario",
  description="Permite actualizar la contraseña de un usuario en especifico. Solo accesible a administradores o staff.",
  responses={
    200: ChangePasswordSerializer,
    400: error_400_serializer,
    403: error_403_serializer
  }
)
class ChangePasswordView(APIResponseMixin, APIView):
  permission_classes = [IsAdmin | IsStaff | IsUserAuthenticated]
  throttle_classes = [SensitiveActionThrottle]

  @LogActionView(
    action_base=get_message("logs", "user_password_update"),
    object_getter=lambda self, request, kwargs, instance: instance.email,
    meta_getter=lambda view, request, view_kwargs, instance: {
      "object_id": instance.id,
      "object_type": GetModelName(instance),
    }
  )
  def put(self, request, user_id, *args, **kwargs):
    # Usa self.get_object() para obtener el usuario y aplicar permisos de DRF
    target = get_object_or_404(User, pk=user_id)

    # Inyectamos el target en el serializer
    serializer = ChangePasswordSerializer(data=request.data, context={
      'request': request,
      'target_user': target
    })

    if serializer.is_valid():
      updated_user = serializer.save()
      resp = self.success_response(
        message=get_message("success", "user_password_update")
      )
      resp.instance = updated_user
      return resp
    
    return self.error_response(
      message=get_message("generic", "bad_request"),
      errors=serializer.errors,
      status_code=status.HTTP_400_BAD_REQUEST
    )

@extend_schema(
  summary="Actualización del idioma del usuario",
  description="Permite actualizar el idioma de un usuario que este autenticado.",
  responses={
    200: ChangeUserLanguageSerializer,
    400: error_400_serializer,
    403: error_403_serializer
  }
)
class ChangeUserLanguageView(APIResponseMixin, APIView):
  permission_classes = [IsUserAuthenticated]

  @LogActionView(
    action_base=get_message("logs", "user_update_language"),
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
      return self.error_response(
        message=get_message("generic", "forbidden"),
        errors={"permission": [get_message("errors", "no_permission_to_modify_user")]},
        status_code=status.HTTP_403_FORBIDDEN
      )

    # Valida payload
    serializer = ChangeUserLanguageSerializer(data=request.data)
    if serializer.is_valid():
      # Asigna y guarda
      target_user.language = serializer.validated_data["language"]
      target_user.save()
      # Arma el Response
      resp = self.success_response(
        data={"language": target_user.language}, 
        message=get_message("success", "user_update_language")
      )
      resp.instance = target_user
      return resp
        
    return self.error_response(
      message=get_message("generic", "bad_request"),
      errors=serializer.errors,
      status_code=status.HTTP_400_BAD_REQUEST
    )