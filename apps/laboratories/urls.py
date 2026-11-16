from rest_framework.routers import DefaultRouter

from apps.laboratories.views import LaboratoryViewSet

router = DefaultRouter()
router.register(r"", LaboratoryViewSet, basename="laboratories")

urlpatterns = router.urls