from rest_framework import serializers

# Base client errors
class error_400_serializer(serializers.Serializer):
    field_errors = serializers.ListField(
        help_text = "Lista de etiquetas (strings) - Errores de validación, campos mal formateados, etc."
    )

class error_401_serializer(serializers.Serializer):
    auth = serializers.ListField(
        help_text = "Lista de etiquetas (strings) - Token inválido, sesión expirada"
    )

class error_403_serializer(serializers.Serializer):
    permission = serializers.ListField(
        help_text = "Lista de etiquetas (strings) - Autenticado pero sin permisos suficientes."
    )

class error_404_serializer(serializers.Serializer):
    field_errors = serializers.ListField(
        help_text = "Lista de etiquetas (strings) - El recurso solicitado no existe."
    )

class error_409_serializer(serializers.Serializer):
    field_errors = serializers.ListField(
        help_text = "Lista de etiquetas (strings) - Recurso duplicado o lógica de negocio rota."
    )

class error_422_serializer(serializers.Serializer):
    field_errors = serializers.ListField(
        help_text = "Lista de etiquetas (strings) - Datos válidos en forma pero inválidos en lógica."
    )

class error_500_serializer(serializers.Serializer):
    server = serializers.ListField(
        help_text = "Lista de etiquetas (strings) - Error inesperado del servidor."
    )

# Authentications
class login_response_serializer(serializers.Serializer):
    from authentication.serializers.auth_serializer import CurrentUserSerializer

    access = serializers.CharField(
        help_text = "Token de acceso."
    )
    refresh = serializers.CharField(
        help_text = "Token de refresh."
    )
    user = CurrentUserSerializer()

class refresh_response_serializer(serializers.Serializer):
    access = serializers.CharField(
        help_text = "Token de acceso."
    )