from datetime import timedelta

from django.core.exceptions import ValidationError
from django.test import TestCase
from django.utils import timezone

from bookings.models import Booking, Provider, Service


class BookingCleanTests(TestCase):
    def setUp(self):
        self.provider = Provider.objects.create(name="Alex")
        self.service = Service.objects.create(
            name="Soch olish",
            duration_minutes=30,
            price=50000,
        )
        self.start = timezone.now() + timedelta(days=1)
        self.end = self.start + timedelta(minutes=30)

    def test_valid_booking_passes_clean(self):
        booking = Booking(
            provider=self.provider,
            service=self.service,
            customer_name="test",
            customer_phone="99 555 5555",
            start_time=self.start,
            end_time=self.end,
        )
        booking.full_clean()

    def test_end_before_start_raises_error(self):
        booking = Booking(
            provider=self.provider,
            service=self.service,
            customer_name="test",
            customer_phone="99 555 5555",
            start_time=self.end,
            end_time=self.start,
        )
        with self.assertRaises(ValidationError):
            booking.full_clean()

    def test_past_booking_raises_error(self):
        past = timezone.now() - timedelta(days=1)
        booking = Booking(
            provider=self.provider,
            service=self.service,
            customer_name="Test",
            customer_phone="900000000",
            start_time=past,
            end_time=past + timedelta(minutes=30),
        )
        with self.assertRaises(ValidationError):
            booking.full_clean()

    def test_overlapping_booking_raises_error(self):
        Booking.objects.create(
            provider=self.provider,
            service=self.service,
            customer_name="Birinchi mijoz",
            customer_phone="900000001",
            start_time=self.start,
            end_time=self.end,
        )

        overlapping_booking = Booking(
            provider=self.provider,
            service=self.service,
            customer_name="Ikkinchi mijoz",
            customer_phone="900000002",
            start_time=self.start + timedelta(minutes=15),
            end_time=self.end + timedelta(minutes=15),
        )

        with self.assertRaises(ValidationError):
            overlapping_booking.full_clean()
