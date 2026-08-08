from rest_framework import serializers

from .models import VeterinaryService


class VeterinaryServiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = VeterinaryService
        fields = '__all__'
        read_only_fields = ('id', 'created_at')

    def validate_duration_minutes(self, value):
        if not 15 <= value <= 240:
            raise serializers.ValidationError('La duración debe estar entre 15 y 240 minutos.')
        return value

    def validate_price(self, value):
        if value < 0:
            raise serializers.ValidationError('El precio no puede ser negativo.')
        return value
