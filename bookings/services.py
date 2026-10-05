from datetime import date, datetime, timedelta

from django.utils import timezone

from .models import Booking, WorkingHours


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
