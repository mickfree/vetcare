from drf_spectacular.utils import extend_schema, extend_schema_view
from rest_framework import viewsets

from .models import Pet
from .serializers import PetSerializer


@extend_schema_view(
    list=extend_schema(tags=['Mascotas'], summary='Listar mis mascotas'),
    retrieve=extend_schema(tags=['Mascotas'], summary='Obtener una mascota'),
    create=extend_schema(tags=['Mascotas'], summary='Registrar una mascota'),
    update=extend_schema(tags=['Mascotas'], summary='Actualizar una mascota'),
    partial_update=extend_schema(tags=['Mascotas'], summary='Actualizar parcialmente una mascota'),
    destroy=extend_schema(tags=['Mascotas'], summary='Eliminar una mascota'),
)
class PetViewSet(viewsets.ModelViewSet):
    queryset = Pet.objects.all()
    serializer_class = PetSerializer

    def get_queryset(self):
        user = self.request.user
        if getattr(user, 'role', None) == 'ADMIN':
            return Pet.objects.all().order_by('id')
        if getattr(user, 'role', None) == 'VET':
            return Pet.objects.filter(
                appointments__veterinarian=user,
            ).distinct().order_by('id')
        return Pet.objects.filter(owner=user).order_by('id')

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)
