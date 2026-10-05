
from rest_framework import serializers

from .models import Booking, Provider, Service


class ServiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Service
        fields = ["id", "name",
                  "duration_minutes", "price", "is_active"]


class ProviderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Provider
        fields = ["id", "name", "bio", "services", "is_active"]


class BookingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Booking
        fields = [
            "id",
            "provider",
            "service",
            "customer_name",
            "customer_phone",
            "start_time",
            "end_time",
            "status",
            "created_at",
        ]
        read_only_fields = ["status", "created_at"]

    def validate(self, attrs):
        booking = Booking(**attrs)
        booking.full_clean(exclude=["status"])
        return attrs
