import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
django.setup()

import threading
from datetime import datetime

from bookings.models import Booking, Provider, Service
from bookings.services import create_booking_safely

provider = Provider.objects.first()
service = Service.objects.first()

start = datetime(2026, 10, 20, 10, 0)  # noqa: DTZ001
end = datetime(2026, 10, 20, 10, 30) # noqa: DTZ001

results = []


def try_book(customer_name):
    try:
        create_booking_safely(
            provider=provider, # type: ignore
            service=service,
            customer_name=customer_name,
            customer_phone="900000000",
            start_time=start,
            end_time=end,
        )
        results.append(f"{customer_name}: MUVAFFAQIYATLI")
    except Exception as e:
        results.append(f"{customer_name}: RAD ETILDI ({e})")


t1 = threading.Thread(target=try_book, args=("Mijoz A",))
t2 = threading.Thread(target=try_book, args=("Mijoz B",))

t1.start()
t2.start()
t1.join()
t2.join()

for r in results:
    print(r)

print()
print("Bazadagi shu vaqtdagi bronlar soni:", Booking.objects.filter(start_time=start).count())