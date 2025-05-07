from rest_framework import status
from rest_framework.views import APIView

from drf_spectacular.utils import extend_schema
from django.conf import settings
from django.contrib.auth.models import Permission
from django.utils.translation import gettext as _

from core.utils.mixins import APIResponseMixin
from core.utils.permissions import IsAdmin, IsStaff, IsUserAuthenticated
from core.base.messages import get_message
from core.base.serializers.responses_serializer import error_400_serializer

from accounts.serializers.permissions_serializer import PermissionNameRequestSerializer, PermissionNameResponseSerializer

@extend_schema(
    summary="Obtener nombres de permisos",
    description="Recibe un array de IDs de permisos y devuelve sus nombres.",
    request=PermissionNameRequestSerializer,
    responses={
        200: PermissionNameResponseSerializer,
        400: error_400_serializer
    }
)
class PermissionNameView(APIResponseMixin, APIView):
  permission_classes = [IsAdmin | IsStaff | IsUserAuthenticated]

  def post(self, request, *args, **kwargs):
    serializer = PermissionNameRequestSerializer(data=request.data)
    if not serializer.is_valid():
      return self.error_response(
        message=get_message("generic", "bad_request"),
        errors=serializer.errors,
        status_code=status.HTTP_400_BAD_REQUEST
      )

    ids = serializer.validated_data['permission_ids']
    permissions = Permission.objects.filter(id__in=ids)
    result = []
    for perm in permissions:
      translated_name = _(perm.name)
      result.append({
        "id": perm.id,
        "name": translated_name
      })
    
    return self.success_response(
      data={"permissions": result},
      message=get_message("success", "permissions_list")
    )

@extend_schema(
    summary="Obtener todos los permisos de apps configuradas",
    description="Devuelve todos los permisos de las apps configuradas en settings.",
    responses={
        200: PermissionNameResponseSerializer,
        400: error_400_serializer
    }
)
class PermissionView(APIResponseMixin, APIView):
  permission_classes = [IsAdmin | IsStaff | IsUserAuthenticated]

  def get(self, request, *args, **kwargs):
    allowed_apps = getattr(settings, "PERMISSION_APPS_ALLOWED", [])
    permissions = Permission.objects.filter(content_type__app_label__in=allowed_apps)
    result = []
    for perm in permissions:
      translated_name = _(perm.name)
      result.append({
        "id": perm.id,
        "name": translated_name
      })

    return self.success_response(
      data={"permissions": result},
      message=get_message("success", "permissions_list")
    )