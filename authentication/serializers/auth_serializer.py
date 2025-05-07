from rest_framework import serializers
from rest_framework_simplejwt.tokens import RefreshToken, TokenError
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from django.contrib.auth import get_user_model

from core.base.messages import get_message

User = get_user_model()

# Serializador de Login
class LoginSerializer(TokenObtainPairSerializer):
  """
  Serializador para login de usuario. Valida las credenciales del usuario y devuelve tokens JWT.
  """

  email = serializers.EmailField()
  password = serializers.CharField(write_only=True, style={'input_type': 'password'})

  def validate(self, attrs):
    email = attrs.get('email')
    password = attrs.get('password')
    user = User.objects.filter(email=email).first()
    if user is None or not user.check_password(password):
      raise serializers.ValidationError(
        {"auth": [get_message("errors", "user_invalid_credentials")]}
      )
    return super().validate(attrs)

# Serializador que regresa informacion del usuario por el Token generado
class UserWithPermissionsSerializer(serializers.ModelSerializer):
  """
  Serializador para obtener los permisos del usuario logueado.
  """
  
  permissions = serializers.SerializerMethodField()

  class Meta:
    model = User
    fields = ['id', 'email', 'first_name', 'last_name', 'user_type', 'permissions']
    read_only_fields = fields
  
  def get_permissions(self, obj):
    return list(obj.get_all_permissions())

# Serializador de logout
class LogoutSerializer(serializers.Serializer):
  """
  Serializador para logout del usuario.
  """
  
  refresh = serializers.CharField(write_only=True)

  def validate(self, attrs):
    refresh_token = attrs.get('refresh')
    if not refresh_token:
      raise serializers.ValidationError(
        {"auth": [get_message("errors", "token_required")]}
      )
    try:
      token = RefreshToken(refresh_token)
      # Optionally, check if token is blacklisted (if using blacklist app)
      if hasattr(token, 'check_blacklist'):
        token.check_blacklist()
    except TokenError:
      raise serializers.ValidationError(
        {"auth": [get_message("errors", "token_invalid")]}
      )
    return attrs

# Serializador para el refresh token
class RefreshTokenSerializer(serializers.Serializer):
  """
  Serializador para refresh del token.
  """
  
  refresh = serializers.CharField(write_only=True)

  def validate(self, attrs):
    refresh_token = attrs.get('refresh')
    if not refresh_token:
      raise serializers.ValidationError(
        {"auth": [get_message("errors", "token_required")]}
      )
    try:
      RefreshToken(refresh_token)
    except TokenError:
      raise serializers.ValidationError(
          {"auth": [get_message("errors", "token_invalid")]}
      )
    return attrs