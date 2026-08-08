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
        return Pet.objects.filter(owner=self.request.user).order_by('id')

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)
