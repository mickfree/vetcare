from django.db import models
from django.conf import settings


class Pet(models.Model):
    class Species(models.TextChoices):
        DOG = 'DOG', 'Perro'
        CAT = 'CAT', 'Gato'
        BIRD = 'BIRD', 'Ave'
        OTHER = 'OTHER', 'Otro'

    class Sex(models.TextChoices):
        MALE = 'MALE', 'Macho'
        FEMALE = 'FEMALE', 'Hembra'

    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='pets')
    name = models.CharField(max_length=100)
    species = models.CharField(max_length=10, choices=Species.choices)
    breed = models.CharField(max_length=100, blank=True)
    birth_date = models.DateField(null=True, blank=True)
    weight = models.DecimalField(max_digits=6, decimal_places=2)
    sex = models.CharField(max_length=10, choices=Sex.choices)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.name} ({self.owner.username})'
