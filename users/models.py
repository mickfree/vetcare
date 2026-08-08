from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    class Role(models.TextChoices):
        CLIENT = 'CLIENT', 'Cliente'
        VET = 'VET', 'Veterinario'
        ADMIN = 'ADMIN', 'Administrador'

    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=20, blank=True)
    address = models.CharField(max_length=255, blank=True)
    role = models.CharField(max_length=10, choices=Role.choices, default=Role.CLIENT)

    def __str__(self):
        return self.username
