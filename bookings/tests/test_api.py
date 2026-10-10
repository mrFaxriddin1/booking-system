from datetime import timedelta

from django.utils import timezone
from rest_framework.test import APITestCase

from bookings.models import Provider, Service


class BookingAPITests(APITestCase):
    def setUp(self):
        self.provider = Provider.objects.create(name="Aziz")
        self.service = Service.objects.create(
            name="Soch olish", duration_minutes=30, price=50000
        )
        self.start = timezone.now() + timedelta(days=1)
        self.end = self.start + timedelta(minutes=30)

    def test_create_booking_via_api(self):
        response = self.client.post(
            "/api/bookings/",
            {
                "provider": self.provider.id,  # type: ignore
                "service": self.service.id,  # type: ignore
                "customer_name": "Test",
                "customer_phone": "900000000",
                "start_time": self.start.isoformat(),
                "end_time": self.end.isoformat(),
            },
        )
        self.assertEqual(response.status_code, 201)

    def test_overlapping_booking_via_api_returns_400(self):
        self.client.post(
            "/api/bookings/",
            {
                "provider": self.provider.id,  # type: ignore
                "service": self.service.id,  # type: ignore
                "customer_name": "Birinchi",
                "customer_phone": "900000001",
                "start_time": self.start.isoformat(),
                "end_time": self.end.isoformat(),
            },
        )

        response = self.client.post(
            "/api/bookings/",
            {
                "provider": self.provider.id,  # type: ignore
                "service": self.service.id,  # type: ignore
                "customer_name": "Ikkinchi",
                "customer_phone": "900000002",
                "start_time": self.start.isoformat(),
                "end_time": self.end.isoformat(),
            },
        )
        self.assertEqual(response.status_code, 400)
