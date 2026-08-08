from rest_framework import serializers

from appointments.models import Appointment
from .models import MedicalRecord


class MedicalRecordSerializer(serializers.ModelSerializer):
    class Meta:
        model = MedicalRecord
        fields = '__all__'
        read_only_fields = ('id', 'veterinarian', 'created_at', 'updated_at')

    def validate_appointment(self, value):
        if value.status != Appointment.Status.COMPLETED:
            raise serializers.ValidationError('Solo se puede crear una historia para una cita completada.')
        if value.veterinarian_id != self.context['request'].user.id:
            raise serializers.ValidationError('La cita no pertenece al veterinario autenticado.')
        return value
