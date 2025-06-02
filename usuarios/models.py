from django.contrib.auth.models import AbstractUser
from django.db import models

class Usuario(AbstractUser):
    class Roles(models.TextChoices):
        PROFESIONAL = 'PROFESIONAL', 'Profesional UAV'
        COORDINACION = 'COORDINACION', 'Coordinación UAV'
        ADMINISTRADOR = 'ADMINISTRADOR', 'Administrador del Sistema'

    rol = models.CharField(
        max_length=20,
        choices=Roles.choices,
        default=Roles.PROFESIONAL,
        verbose_name="Rol del usuario"
    )

    def es_correo_maipu(self):
        return self.email.endswith('@maipu.cl')

    def __str__(self):
        return f"{self.username} ({self.get_rol_display()})"
