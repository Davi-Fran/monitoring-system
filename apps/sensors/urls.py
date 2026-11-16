from rest_framework.routers import DefaultRouter

from apps.sensors.views import SensorModelViewSet, SensorViewSet, SensorReadingViewSet

router = DefaultRouter()
router.register(r"models", SensorModelViewSet, basename="sensor_models")
router.register(r"readings", SensorReadingViewSet, basename="sensor_readings")
router.register(r"", SensorViewSet, basename="sensors")

urlpatterns = router.urls