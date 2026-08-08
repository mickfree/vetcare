from drf_spectacular.utils import extend_schema, extend_schema_view
from rest_framework import viewsets

from .models import Appointment
from .serializers import AppointmentSerializer


@extend_schema_view(
    list=extend_schema(tags=['Citas'], summary='Listar mis citas'),
    retrieve=extend_schema(tags=['Citas'], summary='Obtener una cita'),
    create=extend_schema(tags=['Citas'], summary='Programar una cita'),
    update=extend_schema(tags=['Citas'], summary='Actualizar una cita'),
    partial_update=extend_schema(tags=['Citas'], summary='Actualizar parcialmente una cita'),
    destroy=extend_schema(tags=['Citas'], summary='Eliminar una cita'),
)
class AppointmentViewSet(viewsets.ModelViewSet):
    queryset = Appointment.objects.all()
    serializer_class = AppointmentSerializer

    def get_queryset(self):
        user = self.request.user
        queryset = Appointment.objects.select_related('pet', 'veterinarian', 'service')
        if getattr(user, 'role', None) == 'VET':
            return queryset.filter(veterinarian=user).order_by('scheduled_at')
        if getattr(user, 'role', None) == 'ADMIN':
            return queryset.order_by('scheduled_at')
        return queryset.filter(pet__owner=user).order_by('scheduled_at')
