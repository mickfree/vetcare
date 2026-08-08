from django.contrib.auth import get_user_model
from drf_spectacular.utils import extend_schema, extend_schema_view
from rest_framework import generics, permissions, viewsets
from rest_framework_simplejwt.views import TokenObtainPairView

from .serializers import RegisterSerializer, UserSerializer


@extend_schema(tags=['Autenticación'], summary='Registrar un usuario')
class RegisterView(generics.CreateAPIView):
    queryset = get_user_model().objects.all()
    serializer_class = RegisterSerializer
    permission_classes = [permissions.AllowAny]


@extend_schema(tags=['Autenticación'], summary='Iniciar sesión y obtener tokens JWT')
class LoginView(TokenObtainPairView):
    permission_classes = [permissions.AllowAny]


@extend_schema_view(
    list=extend_schema(tags=['Usuarios'], summary='Listar usuarios'),
    retrieve=extend_schema(tags=['Usuarios'], summary='Obtener un usuario'),
    create=extend_schema(tags=['Usuarios'], summary='Crear un usuario'),
    update=extend_schema(tags=['Usuarios'], summary='Actualizar un usuario'),
    partial_update=extend_schema(tags=['Usuarios'], summary='Actualizar parcialmente un usuario'),
    destroy=extend_schema(tags=['Usuarios'], summary='Eliminar un usuario'),
)
class UserViewSet(viewsets.ModelViewSet):
    queryset = get_user_model().objects.all().order_by('id')
    serializer_class = UserSerializer
