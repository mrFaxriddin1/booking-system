from celery import shared_task


@shared_task
def ping():
    print("celery ishlayabdi")
    return "pong"


@shared_task
def send_booking_reminder(booking_id: int):
    from .models import Booking

    try:
        booking = Booking.objects.get(pk=booking_id)
    except Booking.DoesNotExist:
        return f"Booking {booking_id} topilmadi, eslatma yuborilmadi"

    if booking.status == Booking.Status.CANCELLED:
        return f"Booking {booking_id} bekor qilingan, eslatma yuborilmadi"

    print(
        f"[ESLATMA] {booking.customer_name}, sizning {booking.service.name} "
        f"xizmatingiz {booking.start_time} da boshlanadi"
    )
    return f"Eslatma yuborildi: booking {booking_id}"
