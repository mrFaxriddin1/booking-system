from django.contrib import admin

from .models import Booking, Provider, Service, WorkingHours

# Register your models here.

admin.site.register(Service)
admin.site.register(Provider)
admin.site.register(WorkingHours)
admin.site.register(Booking)
