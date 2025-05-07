from rest_framework import serializers

class PermissionNameRequestSerializer(serializers.Serializer):
  """
  Serializador para obtener el nombre de los permisos mandados en el body por un listado de ID's
  """
  
  permission_ids = serializers.ListField(
    child=serializers.IntegerField(min_value=1),
    allow_empty=False,
    required=True
  )

class PermissionNameResponseSerializer(serializers.Serializer):
  id = serializers.IntegerField()
  name = serializers.CharField()