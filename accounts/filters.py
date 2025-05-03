import django_filters
from django.contrib.auth import get_user_model

User = get_user_model()

class UserFilter(django_filters.FilterSet):
  """
  Filtro para el modelo User.
  Permite filtrar por email, nombre, apellido y estado activo.
  Puedes extenderlo fácilmente con más campos según tus necesidades.
  """

  email = django_filters.CharFilter(field_name="email", lookup_expr="icontains")
  first_name = django_filters.CharFilter(field_name="first_name", lookup_expr="icontains")
  last_name = django_filters.CharFilter(field_name="last_name", lookup_expr="icontains")
  is_active = django_filters.BooleanFilter(field_name="is_active")
  user_type = django_filters.CharFilter(field_name="user_type", choices=User.USER_TYPE_CHOICES)

  class Meta:
    model = User
    fields = ['email', 'first_name', 'last_name', 'is_active', 'user_type']