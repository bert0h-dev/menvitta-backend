from rest_framework.serializers import Serializer, ModelSerializer, EmailField, CharField, ValidationError
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

  email = EmailField()
  password = CharField(write_only=True, style={'input_type': 'password'})

  def validate(self, attrs):
    email = attrs.get('email')
    password = attrs.get('password')
    user = User.objects.filter(email=email).first()
    if user is None or not user.check_password(password):
      raise ValidationError(
        {"auth": [get_message("errors", "user_invalid_credentials")]}
      )
    return super().validate(attrs)

# Serializador que regresa informacion del usuario por el Token generado
class CurrentUserSerializer(ModelSerializer):
  class Meta:
    model = User
    fields = ['id', 'email', 'first_name', 'last_name', 'user_type']
    read_only_fields = fields

# Serializador de logout
class LogoutSerializer(Serializer):
  refresh = CharField(write_only=True)

  def validate(self, attrs):
    refresh_token = attrs.get('refresh')
    if not refresh_token:
      raise ValidationError(
        {"auth": [get_message("errors", "token_required")]}
      )
    try:
      token = RefreshToken(refresh_token)
      # Optionally, check if token is blacklisted (if using blacklist app)
      if hasattr(token, 'check_blacklist'):
        token.check_blacklist()
    except TokenError:
      raise ValidationError(
        {"auth": [get_message("errors", "token_invalid")]}
      )
    return attrs

# Serializador para el refresh token
class RefreshTokenSerializer(Serializer):
  refresh = CharField(write_only=True)

  def validate(self, attrs):
    refresh_token = attrs.get('refresh')
    if not refresh_token:
      raise ValidationError(
        {"auth": [get_message("errors", "token_required")]}
      )
    return attrs