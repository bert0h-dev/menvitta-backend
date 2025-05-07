from rest_framework import serializers

from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group, Permission

from core.base.messages import get_message

User = get_user_model()

class RolesSerializer(serializers.ModelSerializer):
  """
  Serializador para el manejo de los roles del sistema.

  Campos:
    permissions (list[int]): Lista de IDs de permisos (PrimaryKey) requeridos para el rol.
  """

  permissions = serializers.PrimaryKeyRelatedField(
    queryset=Permission.objects.all(),
    many=True,
    required=True
  )
  user_count = serializers.IntegerField(read_only=True, required=False)

  class Meta:
    model = Group
    fields = ['id', 'name', 'permissions', 'user_count']
  
  def validate_name(self, value):
    stripped_value = value.strip() if value else value
    if not stripped_value:
      raise serializers.ValidationError(
        {"name": [get_message("errors", "role_empty")]}
      )
    if Group.objects.exclude(id=self.instance.id if self.instance else None).filter(name=stripped_value).exists():
      raise serializers.ValidationError(
        {"name": [get_message("errors", "role_do_exists")]}
      )
    return stripped_value
  
  def create(self, validated_data):
        permissions = validated_data.pop('permissions', [])
        group = Group.objects.create(**validated_data)
        group.permissions.set(permissions)
        return group

  def update(self, instance, validated_data):
      permissions = validated_data.pop('permissions', None)
      instance.name = validated_data.get('name', instance.name)
      instance.save()
      if permissions is not None:
          instance.permissions.set(permissions)
      return instance

class AssignRoleSerializer(serializers.Serializer):
  """
  Serializador para la asignacion de un rol a un usuario.
  """

  user_id = serializers.PrimaryKeyRelatedField(
    queryset=User.objects.all(),
    required=True,
    write_only=True
  )
  role_id = serializers.PrimaryKeyRelatedField(
    queryset=Group.objects.all(),
    required=True,
    write_only=True
  )

  def validate(self, attrs):
    user = attrs['user_id']
    group = attrs['role_id']
    if group in user.groups.all():
      raise serializers.ValidationError({
        "role_id": [get_message("errors", "role_already_assigned")]
      })
    return attrs
  
  def save(self, **kwargs):
    user = self.validated_data['user_id']
    group = self.validated_data['role_id']
    user.groups.add(group)
    return user

class RemoveRoleSerializer(serializers.Serializer):
  """
  Serializador para remover un rol a un usuario.
  """

  user_id = serializers.PrimaryKeyRelatedField(
    queryset=User.objects.all(),
    required=True,
    write_only=True
  )
  role_id = serializers.PrimaryKeyRelatedField(
    queryset=Group.objects.all(),
    required=True,
    write_only=True
  )

  def validate(self, attrs):
    user = attrs['user_id']
    group = attrs['role_id']
    if group not in user.groups.all():
      raise serializers.ValidationError({
        "role_id": [get_message("errors", "role_not_assigned")]
      })
    return attrs

  def save(self, **kwargs):
    user = self.validated_data['user_id']
    group = self.validated_data['role_id']
    user.groups.remove(group)
    return user