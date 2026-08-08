from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import VeterinaryServiceViewSet

router = DefaultRouter()
router.register('services', VeterinaryServiceViewSet, basename='service')

urlpatterns = [path('', include(router.urls))]
