from django.db import models
from django.conf import settings
from django.utils.translation import gettext_lazy as _

class AccessLog(models.Model):
  """
  Modelo para registrar logs de acceso y acciones de usuarios en el sistema.
  Guarda información relevante para auditoría y seguridad.
  """

  user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True, related_name='access_logs')
  method = models.CharField(max_length=10)
  path = models.TextField()
  action = models.TextField()
  status_code = models.PositiveIntegerField(null=True, blank=True)
  message = models.TextField(null=True, blank=True)
  ip_address = models.GenericIPAddressField(null=True, blank=True)
  user_agent = models.TextField(blank=True, null=True)
  object_id = models.PositiveIntegerField(null=True, blank=True)
  object_type = models.CharField(max_length=50, null=True, blank=True)
  created_at = models.DateTimeField(auto_now_add=True)

  class Meta:
    verbose_name = _("access log")
    verbose_name_plural = _("access logs")
    permissions = [
      ("can_export", _("Can export access logs")),
    ]
    ordering = ['-created_at']
    db_table = 'core_access_log'
    indexes = [
      models.Index(fields=['user']),
      models.Index(fields=['created_at']),
      models.Index(fields=['action']),
      models.Index(fields=['method', 'path']),
    ]
    
  def __str__(self):
    return f"{self.user} - {self.method} {self.path} ({self.status_code})"