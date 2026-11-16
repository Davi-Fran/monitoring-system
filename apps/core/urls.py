from django.urls import path, include

from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView

urlpatterns = [
    path("laboratories/", include("apps.laboratories.urls")),
    path("microcontrollers/", include("apps.devices.urls")),
    path("sensors/", include("apps.sensors.urls")),
    path("users/", include("apps.accounts.urls")),

    path("token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("token/refresh/", TokenRefreshView.as_view(), name="refresh_token"),

    path("docs/", SpectacularAPIView.as_view(), name="schema"),
    path("docs/swagger/", SpectacularSwaggerView.as_view(), name="swagger-ui"),
]