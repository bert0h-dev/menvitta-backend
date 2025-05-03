from django.db import models
from django.contrib.auth.models import AbstractUser, PermissionsMixin, BaseUserManager

from config.settings.base import LANGUAGES

class CustomUserManager(BaseUserManager):
  def create_user(self, email, username=None, password=None, **extra_fields):
    if not email:
      raise ValueError("El correo es obligatorio")
    if password is None:
      raise ValueError("La contraseña es obligatoria")
    
    email = self.normalize_email(email)
    user = self.model(email=email, username=username, **extra_fields)
    user.set_password(password)
    user.save(using=self._db)
    return user
  
  def create_superuser(self, email, username=None, password=None, **extra_fields):
    extra_fields.setdefault("is_staff", True)
    extra_fields.setdefault("is_superuser", True)
    if password is None:
      raise ValueError("La contraseña es obligatoria para el superusuario")
    return self.create_user(email, username, password, **extra_fields)

class User(AbstractUser, PermissionsMixin):
  USER_TYPE_CHOICES = (
    ('admin', 'Administrador'),
    ('staff', 'Staff'),
  )

  # Identificacion
  email = models.EmailField(unique=True)
  username = models.CharField(max_length=150, unique=True, null=True, blank=True)
  first_name = models.CharField(max_length=150)
  last_name = models.CharField(max_length=150)
  user_type = models.CharField(max_length=20, choices=USER_TYPE_CHOICES, default='staff')

  # Preferencias
  language = models.CharField(max_length=10, choices=LANGUAGES, default='es')
  timezone = models.CharField(max_length=50, default='America/Mexico_City')

  # Seguridad
  password_changed = models.BooleanField(default=False)
  last_ip = models.GenericIPAddressField(null=True, blank=True)

  # Sistema
  is_active = models.BooleanField(default=True)
  is_staff = models.BooleanField(default=False)
  date_joined = models.DateTimeField(auto_now_add=True)
  last_activity = models.DateTimeField(null=True, blank=True)

  objects = CustomUserManager()

  USERNAME_FIELD = 'email'
  REQUIRED_FIELDS = ['first_name', 'last_name']

  class Meta:
    db_table = 'accounts_user'
    ordering = ['-date_joined']

  def __str__(self):
    return self.email
  
  def get_full_name(self):
    return f"{self.first_name} {self.last_name or ''}".strip()
  
  def set_password(self, raw_password):
    super().set_password(raw_password)
    self.password_changed = True