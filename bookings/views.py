from datetime import datetime

from rest_framework import viewsets
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Booking, Provider, Service
from .serializers import BookingSerializer, ProviderSerializer, ServiceSerializer
from .services import get_available_slots

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


class AvailableSlotsView(APIView):
    def get(self, request):
        provider_id = request.query_params.get("provider")
        service_id = request.query_params.get("service")
        date_str = request.query_params.get("date")

        if not provider_id or not service_id or not date_str:
            raise ValidationError(
                "provider, service va date parametrlari majburiy"
            )

        try:
            provider = Provider.objects.get(pk=provider_id)
        except Provider.DoesNotExist:
            raise ValidationError(f"Provider id={provider_id} topilmadi.")

        try:
            service = Service.objects.get(pk=service_id)
        except Service.DoesNotExist:
            raise ValidationError(f"Service id={service_id} topilmadi.")

        try:
            target_date = datetime.strptime(date_str, "%Y-%m-%d").date()  # noqa: DTZ007
        except ValueError:
            raise ValidationError("date formati YYYY-MM-DD bo'lishi kerak.")

        slots = get_available_slots(provider, service, target_date)

        return Response({"slots": [slot.isoformat() for slot in slots]})
