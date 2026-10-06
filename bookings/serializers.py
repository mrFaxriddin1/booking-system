
from rest_framework import serializers

from django.core.exceptions import ValidationError as DjangoValidationError
from rest_framework.exceptions import ValidationError as DRFValidationError

from .models import Booking, Provider, Service
from .services import create_booking_safely


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

    def create(self, validated_data):
        try:
            return create_booking_safely(**validated_data)
        except DjangoValidationError as e:
            raise DRFValidationError(e.message_dict if hasattr(
                e, "message_dict") else e.messages)
