from datetime import date, datetime, timedelta

from django.contrib import messages
from django.shortcuts import redirect, render
from rest_framework import viewsets
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Booking, Provider, Service
from .serializers import BookingSerializer, ProviderSerializer, ServiceSerializer
from .services import create_booking_safely, get_available_slots

# Create your views here.


def home(request):
    services = Service.objects.filter(is_active=True)
    providers = Provider.objects.filter(is_active=True)
    return render(request, "bookings/home.html", {
        "services": services,
        "providers": providers,
    })


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
            target_date = datetime.strptime(date_str, "%Y-%m-%d").date()
        except ValueError:
            raise ValidationError("date formati YYYY-MM-DD bo'lishi kerak.")

        slots = get_available_slots(provider, service, target_date)

        return Response({"slots": [slot.isoformat() for slot in slots]})


def provider_detail(request, provider_id):
    provider = Provider.objects.get(pk=provider_id, is_active=True)
    services = provider.services.filter(is_active=True)

    if request.method == "POST":
        service = services.get(pk=request.POST["service_id"])
        slot_start = datetime.fromisoformat(request.POST["slot_start"])
        slot_end = slot_start + timedelta(minutes=service.duration_minutes)

        try:
            create_booking_safely(
                provider=provider,
                service=service,
                customer_name=request.POST["customer_name"],
                customer_phone=request.POST["customer_phone"],
                start_time=slot_start,
                end_time=slot_end,
            )
            messages.success(request, "Bron muvaffaqiyatli yaratildi!")
            return redirect("provider-page", provider_id=provider.pk)
        except ValidationError as e:
            messages.error(request, str(e))
            return redirect("provider-page", provider_id=provider.pk)

    selected_date_str = request.GET.get("date")
    selected_service_id = request.GET.get("service")

    slots = []
    selected_date = None
    selected_service = None

    if selected_date_str and selected_service_id:
        selected_date = datetime.strptime(selected_date_str, "%Y-%m-%d").date()
        selected_service = services.get(pk=selected_service_id)
        slots = get_available_slots(provider, selected_service, selected_date)

    return render(request, "bookings/provider_detail.html", {
        "provider": provider,
        "services": services,
        "slots": slots,
        "selected_date": selected_date,
        "selected_service": selected_service,
        "today": date.today(),
    })
