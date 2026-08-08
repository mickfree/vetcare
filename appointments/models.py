from django.db import models
from django.conf import settings


class Appointment(models.Model):
    class Status(models.TextChoices):
        PENDING = 'PENDING', 'Pendiente'
        CONFIRMED = 'CONFIRMED', 'Confirmada'
        IN_PROGRESS = 'IN_PROGRESS', 'En atención'
        COMPLETED = 'COMPLETED', 'Completada'
        CANCELED = 'CANCELED', 'Cancelada'

    pet = models.ForeignKey('pets.Pet', on_delete=models.CASCADE, related_name='appointments')
    veterinarian = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, related_name='vet_appointments')
    service = models.ForeignKey('services.VeterinaryService', on_delete=models.PROTECT, related_name='appointments')
    scheduled_at = models.DateTimeField()
    status = models.CharField(max_length=15, choices=Status.choices, default=Status.PENDING)
    reason = models.TextField()
    observations = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'Cita #{self.pk} - {self.pet.name}'
