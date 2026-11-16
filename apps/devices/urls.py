from rest_framework.routers import DefaultRouter

from apps.devices.views import MicroControllerModelViewSet, MicroControllerViewSet

router = DefaultRouter()
router.register(r"models", MicroControllerModelViewSet, basename="micro_controller_models")
router.register(r"", MicroControllerViewSet, basename="micro_controllers")

urlpatterns = router.urls