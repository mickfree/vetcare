from drf_spectacular.utils import extend_schema, extend_schema_view
from rest_framework import viewsets

from .models import MedicalRecord
from .serializers import MedicalRecordSerializer


@extend_schema_view(
    list=extend_schema(tags=['Historias clínicas'], summary='Listar historias clínicas'),
    retrieve=extend_schema(tags=['Historias clínicas'], summary='Obtener una historia clínica'),
    create=extend_schema(tags=['Historias clínicas'], summary='Crear una historia clínica'),
    update=extend_schema(tags=['Historias clínicas'], summary='Actualizar una historia clínica'),
    partial_update=extend_schema(tags=['Historias clínicas'], summary='Actualizar parcialmente una historia clínica'),
    destroy=extend_schema(tags=['Historias clínicas'], summary='Eliminar una historia clínica'),
)
class MedicalRecordViewSet(viewsets.ModelViewSet):
    queryset = MedicalRecord.objects.all()
    serializer_class = MedicalRecordSerializer

    def get_queryset(self):
        user = self.request.user
        queryset = MedicalRecord.objects.select_related('appointment', 'veterinarian')
        if getattr(user, 'role', None) == 'ADMIN':
            return queryset.order_by('-created_at')
        if getattr(user, 'role', None) == 'VET':
            return queryset.filter(veterinarian=user).order_by('-created_at')
        return queryset.filter(appointment__pet__owner=user).order_by('-created_at')

    def perform_create(self, serializer):
        serializer.save(veterinarian=self.request.user)
