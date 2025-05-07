from rest_framework import status
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet

from drf_spectacular.utils import extend_schema, extend_schema_view, OpenApiExample
from django.db.models import Count
from django.contrib.auth.models import Group

from core.base.messages import get_message
from core.base.common import GetModelName
from core.base.pagination import BasePagination
from core.base.serializers.responses_serializer import error_400_serializer
from core.utils.mixins import APIResponseMixin
from core.utils.decorators import LogActionView
from core.utils.permissions import IsAdmin, IsStaff

from accounts.serializers.roles_serializer import RolesSerializer, AssignRoleSerializer, RemoveRoleSerializer

@extend_schema_view(
  list=extend_schema(
    summary="Listar roles del sistema",
    description="Permite listar los roles del sistema. Solo accesible a administradores o staff.",
    responses={
      200: RolesSerializer
    }
  ),
  create=extend_schema(
    summary="Crear un rol",
    description="Permite crear roles en el sistema. Solo accesible a administradores o staff.",
    responses={
      200: RolesSerializer,
      400: error_400_serializer
    }
  ),
  retrieve=extend_schema(
    summary="Detalle de un rol",
    description="Permite ver el detalle de un rol en espeficio con los permisos ligados. Solo accesible a administradores o staff.",
  ),
  update=extend_schema(
    summary="Actualización de la información de un rol",
    description="Permite actualizar la información de un rol en especifico. Solo accesible a administradores o staff.",
    responses={
      200: RolesSerializer,
      400: error_400_serializer
    }
  ),
  partial_update=extend_schema(
    summary="Actualización de información parcial de un rol",
    description="Permite actualizar la información de manera parcial de un rol en especifico. Solo accesible a administradores o staff.",
    responses={
      200: RolesSerializer,
      400: error_400_serializer
    }
  ),
  destroy=extend_schema(
    summary="Eliminar un rol del sistema",
    description="Permite eliminar un rol dentro del sistema. Solo accesible a administradores o staff.",
    responses={
      204: OpenApiExample("Response", value={"status_code": "204"}, response_only=True, status_codes=["204"]),
      400: error_400_serializer
    }
  )
)
class RoleViewSet(APIResponseMixin, ModelViewSet):
  serializer_class = RolesSerializer
  permission_classes = [IsAdmin | IsStaff]
  pagination_class = BasePagination

  def get_queryset(self):
    return Group.objects.all().annotate(user_count=Count('user')).prefetch_related('user_set')

  @LogActionView(action_base=get_message("logs", "role_list"))
  def list(self, request, *args, **kwargs):
    queryset = self.filter_queryset(self.get_queryset())
    page = self.paginate_queryset(queryset)

    if page is not None:
      serializer = self.get_serializer(page, many=True)
      return self.success_response(
        data=self.get_paginated_response(serializer.data).data, 
        message=get_message("success", "role_list")
      )
      
    serializer = self.get_serializer(queryset, many=True)
    return self.success_response(
      data=serializer.data, 
      message=get_message("success", "role_list")
    )
  
  @LogActionView(
    action_base=get_message("logs", "role_details"),
    object_getter=lambda self, request, kwargs, instance: instance.name,
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
      message=get_message("success", "role_recovered")
    )
  
  @LogActionView(
    action_base=get_message("logs", "role_create"),
    object_getter=lambda self, request, kwargs, instance: instance.name,
    meta_getter=lambda view, request, view_kwargs, instance: {
      "object_id": instance.id,
      "object_type": GetModelName(instance),
    }
  )
  def create(self, request, *args, **kwargs):
    serializer = self.get_serializer(data=request.data)
    if serializer.is_valid():
      self.perform_create(serializer)
      return self.success_response(
        data=serializer.data,
        message=get_message("success", "role_create"),
        status=status.HTTP_201_CREATED
      )
    
    return self.error_response(
      message=get_message("generic", "bad_request"),
      errors=serializer.errors,
      status_code=status.HTTP_400_BAD_REQUEST
    )
  
  @LogActionView(
    action_base=get_message("logs", "role_update"),
    object_getter=lambda self, request, kwargs, instance: instance.name,
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
        message=get_message("success", "role_update")
      )
    
    return self.error_response(
      message=get_message("generic", "bad_request"),
      errors=serializer.errors,
      status_code=status.HTTP_400_BAD_REQUEST
    )
  
  @LogActionView(action_base=get_message("logs", "role_destroy"))
  def destroy(self, request, *args, **kwargs):
    instance = self.get_object()
    if instance.user_set.exists():
      return self.error_response(
        message=get_message("generic", "bad_request"),
        errors={"error": [get_message("errors", "role_do_assign")]},
        status_code=status.HTTP_400_BAD_REQUEST
      )
    
    self.perform_destroy(instance)
    return self.onlystatus_response(
      status_code=status.HTTP_204_NO_CONTENT
    )

@extend_schema(
    summary="Asignar un rol a un usuario",
    description="Permite asignar un rol (Group) a un usuario. Solo accesible a administradores o staff.",
    request=AssignRoleSerializer,
    responses={
        200: AssignRoleSerializer,
        400: error_400_serializer
    }
)
class AssignRoleToUserView(APIResponseMixin, APIView):
  permission_classes = [IsAdmin | IsStaff]
  
  @LogActionView(action_base=get_message("logs", "assign_role_to_user"))
  def post(self, request, *args, **kwargs):
    serializer = AssignRoleSerializer(data=request.data)
    if serializer.is_valid():
      user = serializer.save()
      return self.success_response(
        message=get_message("success", "role_assigned")
      )
    
    return self.error_response(
      message=get_message("generic", "bad_request"),
      errors=serializer.errors,
      status_code=status.HTTP_400_BAD_REQUEST
    )

@extend_schema(
  summary="Remover un rol de un usuario",
  description="Permite remover un rol (Group) de un usuario. Solo accesible a administradores o staff.",
  request=RemoveRoleSerializer,
  responses={
    200: RemoveRoleSerializer,
    400: error_400_serializer
  }
)
class RemoveRoleToUserView(APIResponseMixin, APIView):
  permission_classes = [IsAdmin | IsStaff]

  @LogActionView(action_base=get_message("logs", "remove_role_from_user"))
  def post(self, request, *args, **kwargs):
    serializer = RemoveRoleSerializer(data=request.data)
    if serializer.is_valid():
      user = serializer.save()
      return self.success_response(
        message=get_message("success", "role_removed")
      )
    
    return self.error_response(
      message=get_message("generic", "bad_request"),
      errors=serializer.errors,
      status_code=status.HTTP_400_BAD_REQUEST
    )