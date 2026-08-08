from django.db import models
from django.conf import settings


class MedicalRecord(models.Model):
    appointment = models.OneToOneField('appointments.Appointment', on_delete=models.CASCADE, related_name='medical_record')
    veterinarian = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, related_name='medical_records')
    diagnosis = models.TextField()
    treatment = models.TextField()
    prescription = models.TextField(blank=True)
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'Historia clínica de la cita #{self.appointment_id}'
