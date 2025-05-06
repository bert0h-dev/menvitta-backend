from rest_framework.serializers import Serializer, CharField, ListField

# Base client errors
class error_400_serializer(Serializer):
    field_errors = ListField(
        help_text = "Lista de etiquetas (strings) - Errores de validación, campos mal formateados, etc."
    )

class error_401_serializer(Serializer):
    auth = ListField(
        help_text = "Lista de etiquetas (strings) - Token inválido, sesión expirada"
    )

class error_403_serializer(Serializer):
    permission = ListField(
        help_text = "Lista de etiquetas (strings) - Autenticado pero sin permisos suficientes."
    )

class error_404_serializer(Serializer):
    field_errors = ListField(
        help_text = "Lista de etiquetas (strings) - El recurso solicitado no existe."
    )

class error_409_serializer(Serializer):
    field_errors = ListField(
        help_text = "Lista de etiquetas (strings) - Recurso duplicado o lógica de negocio rota."
    )

class error_422_serializer(Serializer):
    field_errors = ListField(
        help_text = "Lista de etiquetas (strings) - Datos válidos en forma pero inválidos en lógica."
    )

class error_500_serializer(Serializer):
    server = ListField(
        help_text = "Lista de etiquetas (strings) - Error inesperado del servidor."
    )

# Authentications
class login_response_serializer(Serializer):
    from authentication.serializers.auth_serializer import CurrentUserSerializer

    access = CharField(
        help_text = "Token de acceso."
    )
    refresh = CharField(
        help_text = "Token de refresh."
    )
    user = CurrentUserSerializer()

class refresh_response_serializer(Serializer):
    access = CharField(
        help_text = "Token de acceso."
    )