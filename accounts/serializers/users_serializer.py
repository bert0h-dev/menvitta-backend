import re

from rest_framework.serializers import Serializer, ModelSerializer, SerializerMethodField, CharField, ChoiceField, ValidationError

from django.conf import settings
from django.utils import timezone
from django.contrib.auth import get_user_model

from zoneinfo import ZoneInfo

from core.base.messages import MSG_ERRORS

User = get_user_model()

class UserSerializer(ModelSerializer):
  """
  Serializador para listar usuarios, incluyendo la última actividad en la zona horaria del usuario.
  """

  last_activity_local = SerializerMethodField()

  class Meta:
    model = User
    fields = [
      'id', 'email', 'username', 
      'first_name', 'last_name', 
      'user_type', 'is_active', 
      'last_activity', 'last_activity_local', 
      'timezone'
    ]

  def get_last_activity_local(self, obj):
    if not obj.last_activity:
      return None
    
    # Convierte la fecha y hora UTC a la zona horaria del usuario
    try:
      user_tz = ZoneInfo(obj.timezone or "UTC")
    except Exception:
      user_tz = ZoneInfo("UTC")

    dt = obj.last_activity
    # Asegurarnos de que dt tenga tzinfo.UTC
    if timezone.is_naive(dt):
        dt = dt.replace(tzinfo=timezone.utc)

    # Convertir directamente
    local_dt = dt.astimezone(user_tz)
    return local_dt.strftime("%Y-%m-%d %H:%M:%S")
  
class ChangePasswordSerializer(Serializer):
  """
  Serializador para cambiar la contraseña del usuario autenticado.
  """

  current_password = CharField(write_only=True, style={'input_type': 'password'}, required=False)
  new_password = CharField(write_only=True, style={'input_type': 'password'})
  confirm_password = CharField(write_only=True, style={'input_type': 'password'})

  def validate(self, attrs):
    request_user = self.context['request'].user
    target_user = self.context['target_user']

    new_pass = attrs.get('new_password')
    confirm = attrs.get('confirm_password')

    # Si el que edita es el mismo usuario, exigir current_password
    if request_user == target_user:
      current = attrs.get('current_password')
      if not current or not target_user.check_password(current):
        raise ValidationError(MSG_ERRORS['invalid_current_password'])
    
    # Confirma el match
    if new_pass != confirm:
      raise ValidationError(MSG_ERRORS['passwords_do_not_match'])
    
    # Validaciones extra
    if len(new_pass) < 8:
      raise ValidationError(MSG_ERRORS['password_do_short'])
    if not re.search(r"[A-Z]", new_pass):
      raise ValidationError(MSG_ERRORS['password_any_uppercase'])
    if not re.search(r"[a-z]", new_pass):
      raise ValidationError(MSG_ERRORS['password_any_lowercase'])
    if not re.search(r"[0-9]", new_pass):
      raise ValidationError(MSG_ERRORS['password_any_number'])
    if not re.search(r"[!@#$%^&*(),.?\":{}|<>]", new_pass):
      raise ValidationError(MSG_ERRORS['password_any_special'])

    return attrs
  
  def save(self):
    target_user = self.context['target_user']
    target_user.set_password(self.validated_data['new_password']) 
    target_user.save()
    return target_user

class ChangeUserLanguageSerializer(Serializer):
  """
  Serializador para cambiar el idioma del usuario autenticado.
  """

  language = ChoiceField(choices=settings.LANGUAGES, error_messages=MSG_ERRORS['invalid_language'])