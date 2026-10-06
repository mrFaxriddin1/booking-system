from datetime import date, datetime, timedelta

from django.core.exceptions import ValidationError
from django.db import transaction
from django.utils import timezone

from .models import Booking, Provider, WorkingHours
from .tasks import send_booking_reminder


def get_available_slots(provider, service, target_date: date) -> list[datetime]:
    weekday = target_date.weekday()
    duration = timedelta(minutes=service.duration_minutes)

    working_periods = WorkingHours.objects.filter(
        provider=provider, weekday=weekday
    )

    existing_bookings = Booking.objects.filter(
        provider=provider,
        start_time__date=target_date,
    ).exclude(status=Booking.Status.CANCELLED)

    slots = []

    for period in working_periods:
        work_start = timezone.make_aware(
            datetime.combine(target_date, period.start_time))
        work_end = timezone.make_aware(
            datetime.combine(target_date, period.end_time))

        cursor = work_start
        while cursor + duration <= work_end:
            slot_end = cursor + duration

            has_conflict = any(
                cursor < booking.end_time and slot_end > booking.start_time
                for booking in existing_bookings
            )

            if not has_conflict:
                slots.append(cursor)

            cursor += duration

    return slots


def create_booking_safely(*, provider: Provider, service, customer_name, customer_phone, start_time, end_time):
    with transaction.atomic():
        # Provider qatorini qulflaymiz — shu providerga tegishli
        # boshqa so'rov, shu transaction tugaguncha, shu yerda kutib turadi.
        locked_provider = Provider.objects.select_for_update().get(pk=provider.pk)

        conflicts = Booking.objects.filter(
            provider=locked_provider,
            start_time__lt=end_time,
            end_time__gt=start_time,
        ).exclude(status=Booking.Status.CANCELLED)

        if conflicts.exists():
            raise ValidationError("Bu provider uchun bu vaqt oralig'i band.")

        booking = Booking(
            provider=locked_provider,
            service=service,
            customer_name=customer_name,
            customer_phone=customer_phone,
            start_time=start_time,
            end_time=end_time,
        )
        booking.full_clean()
        booking.save()

        reminder_time = start_time - timedelta(hours=1)
        transaction.on_commit(
            lambda: send_booking_reminder.apply_async(
                args=[booking.id], eta=reminder_time)  # type: ignore
        )
        return booking
