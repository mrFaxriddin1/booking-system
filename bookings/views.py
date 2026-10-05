from rest_framework import viewsets

from .models import Booking, Provider, Service
from .serializers import BookingSerializer, ProviderSerializer, ServiceSerializer

# Create your views here.


class ServiceViewSet(viewsets.ModelViewSet):
    queryset = Service.objects.filter(is_active=True)
    serializer_class = ServiceSerializer


class ProviderViewSet(viewsets.ModelViewSet):
    queryset = Provider.objects.filter(is_active=True)
    serializer_class = ProviderSerializer


class BookingViewSet(viewsets.ModelViewSet):
    queryset = Booking.objects.all()
    serializer_class = BookingSerializer
