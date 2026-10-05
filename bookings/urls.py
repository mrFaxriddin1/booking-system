from django.urls import path
from rest_framework.routers import DefaultRouter

from .views import AvailableSlotsView, BookingViewSet, ProviderViewSet, ServiceViewSet

router = DefaultRouter()
router.register("services", ServiceViewSet, basename="service")
router.register("providers", ProviderViewSet, basename="provider")
router.register("bookings", BookingViewSet, basename="booking")

urlpatterns = router.urls + [
    path("available-slots/", AvailableSlotsView.as_view(), name="available-slots"),
]
