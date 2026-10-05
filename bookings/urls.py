from rest_framework.routers import DefaultRouter

from .views import BookingViewSet, ProviderViewSet, ServiceViewSet

router = DefaultRouter()
router.register("services", ServiceViewSet, basename="service")
router.register("providers", ProviderViewSet, basename="provider")
router.register("bookings", BookingViewSet, basename="booking")

urlpatterns = router.urls
