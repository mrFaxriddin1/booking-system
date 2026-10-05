
from django.core.exceptions import ValidationError
from django.db import models

# Create your models here.


class Service(models.Model):
    name = models.CharField(max_length=100)
    duration_minutes = models.PositiveSmallIntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    is_active = models.BooleanField(default=True)

    def __str__(self) -> str:
        return self.name


class Provider(models.Model):
    name = models.CharField(max_length=100)
    bio = models.TextField(blank=True)
    services = models.ManyToManyField(
        Service, blank=True, related_name="providers")
    is_active = models.BooleanField(default=True)

    def __str__(self) -> str:
        return self.name


class WorkingHours(models.Model):
    class Weekday(models.IntegerChoices):
        MONDAY = 0, "Dushanba"
        TUESDAY = 1, "Seshanba"
        WEDNESDAY = 2, "Chorshanba"
        THURSDAY = 3, "Payshanba"
        FRIDAY = 4, "Juma"
        SATURDAY = 5, "Shanba"
        SUNDAY = 6, "Yakshanba"

    provider = models.ForeignKey(
        Provider, on_delete=models.CASCADE, related_name="working_hours"
    )
    weekday = models.PositiveSmallIntegerField(choices=Weekday.choices)
    start_time = models.TimeField()
    end_time = models.TimeField()

    class Meta:
        ordering = ["provider", "weekday", "start_time"]

    def get_weekday_display(self):
        return self.Weekday(self.weekday).label

    def __str__(self) -> str:
        return f"{self.provider} - {self.get_weekday_display()} {self.start_time}-{self.end_time}"


class Booking(models.Model):
    class Status(models.TextChoices):
        PENDING = "pending", "Kutilmoqda"
        CONFIRMED = "confirmed", "Tasdiqlangan"
        CANCELLED = "cancelled", "Bekor qilingan"
        COMPLETED = "completed", "Bajarilgan"

    provider = models.ForeignKey(
        Provider, on_delete=models.PROTECT, related_name="bookings"
    )

    service = models.ForeignKey(
        Service, on_delete=models.PROTECT, related_name="bookings"
    )
    customer_name = models.CharField(max_length=100)
    customer_phone = models.CharField(max_length=20)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    status = models.CharField(
        max_length=20, choices=Status.choices, default=Status.PENDING
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["start_time"]

    def __str__(self) -> str:
        return f"{self.customer_name} - {self.provider} ({self.start_time})"

    def clean(self) -> None:
        if self.start_time and self.end_time and self.start_time >= self.end_time:
            raise ValidationError(
                "Boshlanish vaqti tugash vaqtidan oldin bo'lishi kerak")

        conflicts = Booking.objects.filter(
            provider=self.provider,
            start_time__lt=self.end_time,
            end_time__gt=self.start_time,
        ).exclude(status=Booking.Status.CANCELLED)

        if self.pk:
            conflicts = conflicts.exclude(pk=self.pk)

        if conflicts.exists():
            raise ValidationError("Bu provider uchun bu vaqt oralig'i band.")
