from rest_framework import status
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.tokens import RefreshToken, TokenError

from drf_spectacular.utils import extend_schema, OpenApiExample
from django.contrib.auth import authenticate

from core.base.messages import get_message
from core.base.serializers.responses_serializer import (
  login_response_serializer, refresh_response_serializer,
  error_400_serializer, error_401_serializer, 
  error_403_serializer, error_404_serializer
)
from core.utils.mixins import APIResponseMixin
from core.utils.decorators import LogActionView

from authentication.serializers.auth_serializer import (
  UserWithPermissionsSerializer, 
  LoginSerializer, LogoutSerializer, 
  RefreshTokenSerializer
)

@extend_schema(
  summary="Iniciar sesión",
  description="Permite a un usuario autenticarse y obtener tokens JWT.",
  request=LoginSerializer,
  responses={
    200: login_response_serializer,
    403: error_403_serializer,
    404: error_404_serializer,
  },
)
class LoginView(APIResponseMixin, TokenObtainPairView):
  authentication_classes = []
  permission_classes = [AllowAny]

  @LogActionView(action_base=get_message("logs", "login"))
  def post(self, request):
    serializer = LoginSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)

    email = serializer.validated_data['email']
    password = serializer.validated_data['password']

    user = authenticate(request, username=email, password=password)

    if user is None:
      return self.error_response(
        message=get_message("generic", "not_found"),
        errors={"user": [get_message("errors", "user_invalid_credentials")]},
        status_code=status.HTTP_404_NOT_FOUND
      )
    
    if not user.is_active:
      return self.error_response(
        message=get_message("generic", "forbidden"),
        errors={"permission": [get_message("errors", "user_disabled")]},
        status_code=status.HTTP_403_FORBIDDEN
      )
    
    refresh = RefreshToken.for_user(user)
    access_token = str(refresh.access_token)
    refresh_token = str(refresh)

    user_data = UserWithPermissionsSerializer(user).data

    data = {
      "access": access_token,
      "refresh": refresh_token,
      "user": user_data,
    }

    return self.success_response(
      data=data, 
      message=get_message("success", "login")
    )

@extend_schema(
    summary="Cerrar sesión",
    description="Permite invalidar el token de refresh del usuario.",
    request=LogoutSerializer,
    responses={
      205: OpenApiExample("Response", value={"status_code": "205"}, response_only=True, status_codes=["205"]),
      400: error_400_serializer,
      401: error_401_serializer
    }
)
class LogoutView(APIResponseMixin, APIView):
  @LogActionView(action_base=get_message("logs", "logout"))
  def post(self, request):
    serializer = LogoutSerializer(data=request.data)
    if serializer.is_valid():
      refresh_token = serializer.validated_data['refresh']

      try:
        token = RefreshToken(refresh_token)
        token.blacklist()
      except TokenError:
        return self.error_response(
          message=get_message("generic", "unauthorized"), 
          errors={"auth": [get_message("errors", "token_invalid")]},
          status_code=status.HTTP_401_UNAUTHORIZED
        )
      except Exception:
        return self.error_response(
          message=get_message("generic", "bad_request"), 
          errors={"logout": [get_message("errors", "logout_failed")]},
          status_code=status.HTTP_400_BAD_REQUEST
        )

      return self.onlystatus_response(
        status_code=status.HTTP_205_RESET_CONTENT
      )
    
    return self.error_response(
      message=get_message("generic", "unauthorized"), 
      errors=serializer.errors,
      status_code=status.HTTP_401_UNAUTHORIZED
    )

@extend_schema(
  summary="Refrescar token de acceso",
  description="Permite obtener un nuevo access token usando un refresh token válido.",
  request=RefreshTokenSerializer,
  responses={
    200: refresh_response_serializer,
    400: error_400_serializer,
    401: error_401_serializer
  }
)
class RefreshTokenView(APIResponseMixin, APIView):
  permission_classes = [AllowAny]

  @LogActionView(action_base=get_message("logs", "token_refresh"))
  def post(self, request):
    serializer = RefreshTokenSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    refresh_token = serializer.validated_data['refresh']

    try:
      refresh = RefreshToken(refresh_token)
      access_token = str(refresh.access_token)
    except TokenError:
      return self.error_response(
        message=get_message("generic", "unauthorized"), 
        errors={"auth": [get_message("errors", "token_invalid")]},
        status_code=status.HTTP_401_UNAUTHORIZED
      )
    except Exception:
      return self.error_response(
        message=get_message("generic", "bad_request"), 
        errors={"refresh": [get_message("errors", "refresh_failed")]},
        status_code=status.HTTP_400_BAD_REQUEST
      )
    
    data = {
      "access": access_token
    }
    return self.success_response(
      data=data, 
      message=get_message("success", "token_refresh")
    )