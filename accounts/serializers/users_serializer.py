import re

from rest_framework import serializers

from django.conf import settings
from django.utils import timezone
from django.contrib.auth import get_user_model

from zoneinfo import ZoneInfo, ZoneInfoNotFoundError

from core.base.messages import get_message

User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
  """
  Serializador para manejo de usuarios, incluyendo la última actividad en la zona horaria del usuario.
  """

  last_activity_local = serializers.SerializerMethodField()

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
    except ZoneInfoNotFoundError:
      user_tz = ZoneInfo("UTC")

    dt = obj.last_activity
    # Asegurarnos de que dt tenga tzinfo.UTC
    if timezone.is_naive(dt):
        dt = dt.replace(tzinfo=timezone.utc)

    # Convertir directamente
    local_dt = dt.astimezone(user_tz)
    return local_dt.strftime("%Y-%m-%d %H:%M:%S")

class CustomCreateUserSerializer(serializers.ModelSerializer):
  """
  Serializador para crear un usuario en el sistema.
  """

  password = serializers.CharField(write_only=True, style={'input_type': 'password'})
  password2 = serializers.CharField(write_only=True, style={'input_type': 'password'})
  user_type = serializers.ChoiceField(choices=User.USER_TYPE_CHOICES, default='user')

  class Meta:
    model = User
    fields = ('id', 'email', 'password', 'password2', 'first_name', 'last_name', 'user_type')
    extra_kwargs = {
      'email': {'required': True, 'allow_blank': False},
      'first_name': {'required': True, 'allow_blank': False},
      'last_name': {'required': True, 'allow_blank': False},
    }
  
  def validate_email(self, value):
    qs = User.objects.filter(email__iexact=value)
    if self.instance:
      qs = qs.exclude(pk=self.instance.pk)
    if qs.exists():
      raise serializers.ValidationError(get_message('errors', 'user_invalid_email'))
    return value

  def validate(self, attrs):
    password = attrs.get('password')
    password2 = attrs.get('password2')

    # Confirma el match
    if password != password2:
        raise serializers.ValidationError({
          'password2': get_message('errors', 'passwords_do_not_match')
        })
    
    # Validaciones extra
    if len(password) < 8:
      raise serializers.ValidationError({
        'password': get_message('errors', 'password_do_short')
      })
    if not any(c.isupper() for c in password):
      raise serializers.ValidationError({
        'password': get_message('errors', 'password_any_uppercase')
      })
    if not any(c.islower() for c in password):
      raise serializers.ValidationError({
        'password': get_message('errors', 'password_any_lowercase')
      })
    if not any(c.isdigit() for c in password):
      raise serializers.ValidationError({
        'password': get_message('errors', 'password_any_number')
      })
    if not any(c in '!@#$%^&*()-_=+[]{}|;:,.<>?/' for c in password):
      raise serializers.ValidationError({
        'password': get_message('errors', 'password_any_special')
      })
    
    return attrs
  
  def create(self, validated_data):
    validated_data.pop('password2')
    password = validated_data.pop('password')
    user_type = validated_data.pop('user_type', 'user')

    # Asignacion de banderas segun el tipo de usuario
    is_staff = False
    is_superuser = False
    if user_type == 'admin':
      is_staff = True
      is_superuser = True
    elif user_type == 'staff':
      is_staff = True
      is_superuser = False
    elif user_type == 'user':
      is_staff = False
      is_superuser = False

    user = User(
      **validated_data,
      user_type=user_type,
      is_staff=is_staff,
      is_superuser=is_superuser
    )
    user.set_password(password)
    user.save()
    return user

class ChangePasswordSerializer(serializers.Serializer):
  """
  Serializador para cambiar la contraseña del usuario autenticado.
  """

  current_password = serializers.CharField(write_only=True, style={'input_type': 'password'}, required=False)
  new_password = serializers.CharField(write_only=True, style={'input_type': 'password'})
  confirm_password = serializers.CharField(write_only=True, style={'input_type': 'password'})

  def validate(self, attrs):
    request_user = self.context['request'].user
    target_user = self.context['target_user']

    new_pass = attrs.get('new_password')
    confirm = attrs.get('confirm_password')

    # Ensure required fields are present
    if new_pass is None:
      raise serializers.ValidationError({
        "new_password": get_message('errors', 'field_required')
      })
    if confirm is None:
      raise serializers.ValidationError({
        "confirm_password": get_message('errors', 'field_required')
      })
    
    # Si el que edita es el mismo usuario, exigir current_password
    if request_user == target_user:
      current = attrs.get('current_password')
      if not current or not target_user.check_password(current):
        raise serializers.ValidationError({
          "current_password": get_message('errors', 'invalid_current_password')
        })
    
    # Confirma el match
    if new_pass != confirm:
      raise serializers.ValidationError({
        "confirm_new_password": get_message('errors', 'passwords_do_not_match')
      })

    # Validaciones extra
    if len(new_pass) < 8:
      raise serializers.ValidationError({
        "new_password": get_message('errors', 'password_do_short')
      })
    if not re.search(r"[A-Z]", new_pass):
      raise serializers.ValidationError({
        "new_password": get_message('errors', 'password_any_uppercase')
      })
    if not re.search(r"[a-z]", new_pass):
      raise serializers.ValidationError({
        "new_password": get_message('errors', 'password_any_lowercase')
      })
    if not re.search(r"[0-9]", new_pass):
      raise serializers.ValidationError({
        "new_password": get_message('errors', 'password_any_number')
      })
    if not re.search(r"[!@#$%^&*(),.?\":{}|<>]", new_pass):
      raise serializers.ValidationError({
        "new_password": get_message('errors', 'password_any_special')
      })

    return attrs
  
  def save(self):
    target_user = self.context['target_user']
    target_user.set_password(self.validated_data['new_password']) 
    target_user.save()
    return target_user

class ChangeUserLanguageSerializer(serializers.Serializer):
  """
  Serializador para cambiar el idioma del usuario autenticado.
  """

  language = serializers.ChoiceField(choices=settings.LANGUAGES)