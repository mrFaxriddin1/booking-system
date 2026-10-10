from datetime import timedelta

from django.db.models.signals import post_save
from django.db import transaction
from django.dispatch import receiver

from .models import Booking
from .tasks import send_booking_reminder


@receiver(post_save, sender=Booking)
def schedule_reminder_on_create(sender, instance, created, **kwargs):
    if not created:
        return

    reminder_time = instance.start_time - timedelta(hours=1)
    transaction.on_commit(
        lambda: send_booking_reminder.apply_async(
            args=[instance.id], eta=reminder_time)
    )
