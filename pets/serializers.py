from django.utils import timezone
from rest_framework import serializers

from .models import Pet


class PetSerializer(serializers.ModelSerializer):
    class Meta:
        model = Pet
        fields = '__all__'
        read_only_fields = ('id', 'owner', 'created_at')

    def validate_birth_date(self, value):
        if value and value > timezone.localdate():
            raise serializers.ValidationError('La fecha de nacimiento no puede estar en el futuro.')
        return value

    def validate_weight(self, value):
        if value <= 0:
            raise serializers.ValidationError('El peso debe ser mayor que cero.')
        return value
