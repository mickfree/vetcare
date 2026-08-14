from django.utils import timezone
from rest_framework import serializers

from .models import Appointment


class AppointmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Appointment
        fields = '__all__'
        read_only_fields = ('id', 'created_at', 'updated_at')

    def validate(self, attrs):
        request = self.context['request']
        pet = attrs.get('pet', getattr(self.instance, 'pet', None))
        veterinarian = attrs.get('veterinarian', getattr(self.instance, 'veterinarian', None))
        service = attrs.get('service', getattr(self.instance, 'service', None))
        scheduled_at = attrs.get('scheduled_at', getattr(self.instance, 'scheduled_at', None))
        role = getattr(request.user, 'role', None)

        if (
            pet
            and role == 'CLIENT'
            and pet.owner_id != request.user.id
        ):
            raise serializers.ValidationError({'pet': 'La mascota no pertenece al usuario autenticado.'})
        if (
            role == 'CLIENT'
            and 'status' in attrs
            and attrs['status'] != (
                self.instance.status if self.instance else Appointment.Status.PENDING
            )
        ):
            raise serializers.ValidationError({
                'status': 'Solo un veterinario o administrador puede cambiar el estado de la cita.'
            })
        if veterinarian and veterinarian.role != 'VET':
            raise serializers.ValidationError({'veterinarian': 'El usuario seleccionado no es veterinario.'})
        if service and not service.is_active:
            raise serializers.ValidationError({'service': 'El servicio seleccionado no está activo.'})
        schedule_changed = (
            not self.instance
            or scheduled_at != self.instance.scheduled_at
        )
        if scheduled_at and schedule_changed and scheduled_at <= timezone.now():
            raise serializers.ValidationError({'scheduled_at': 'La cita debe programarse en el futuro.'})

        conflict = Appointment.objects.filter(
            veterinarian=veterinarian,
            scheduled_at=scheduled_at,
        ).exclude(status=Appointment.Status.CANCELED)
        if self.instance:
            conflict = conflict.exclude(pk=self.instance.pk)
        if veterinarian and scheduled_at and conflict.exists():
            raise serializers.ValidationError({'scheduled_at': 'El veterinario ya tiene una cita en ese horario.'})
        return attrs
