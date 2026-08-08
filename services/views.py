from drf_spectacular.utils import extend_schema, extend_schema_view
from rest_framework import viewsets

from .models import VeterinaryService
from .serializers import VeterinaryServiceSerializer


@extend_schema_view(
    list=extend_schema(tags=['Servicios'], summary='Listar servicios veterinarios'),
    retrieve=extend_schema(tags=['Servicios'], summary='Obtener un servicio veterinario'),
    create=extend_schema(tags=['Servicios'], summary='Crear un servicio veterinario'),
    update=extend_schema(tags=['Servicios'], summary='Actualizar un servicio veterinario'),
    partial_update=extend_schema(tags=['Servicios'], summary='Actualizar parcialmente un servicio'),
    destroy=extend_schema(tags=['Servicios'], summary='Eliminar un servicio veterinario'),
)
class VeterinaryServiceViewSet(viewsets.ModelViewSet):
    queryset = VeterinaryService.objects.all().order_by('id')
    serializer_class = VeterinaryServiceSerializer
