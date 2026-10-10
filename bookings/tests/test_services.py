import threading
from datetime import timedelta

from django.db import connections
from django.test import TransactionTestCase
from django.utils import timezone

from bookings.models import Booking, Provider, Service
from bookings.services import create_booking_safely


class RaceConditionTests(TransactionTestCase):
    def setUp(self):
        self.provider = Provider.objects.create(name="Aziz")
        self.service = Service.objects.create(
            name="Soch olish", duration_minutes=30, price=50000
        )
        self.start = timezone.now() + timedelta(days=1)
        self.end = self.start + timedelta(minutes=30)

    def test_concurrent_bookings_only_one_succeeds(self):
        results = []

        def try_book(customer_name):
            try:
                create_booking_safely(
                    provider=self.provider,
                    service=self.service,
                    customer_name=customer_name,
                    customer_phone="900000000",
                    start_time=self.start,
                    end_time=self.end,
                )
                results.append("success")
            except Exception:  # noqa: BLE001
                results.append("failed")
            finally:
                connections.close_all()

        t1 = threading.Thread(target=try_book, args=("Mijoz A",))
        t2 = threading.Thread(target=try_book, args=("Mijoz B",))

        t1.start()
        t2.start()
        t1.join()
        t2.join()

        self.assertEqual(results.count("success"), 1)
        self.assertEqual(results.count("failed"), 1)
        self.assertEqual(Booking.objects.filter(start_time=self.start).count(), 1)
