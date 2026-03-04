from django.urls import include, path
from rest_framework.routers import DefaultRouter

from tenants.views import SwitchTenantView, TenantViewSet

router = DefaultRouter()
router.register(r"", TenantViewSet, basename="tenants")

urlpatterns = [
    path("switch/", SwitchTenantView.as_view(), name="switch"),
    path("", include(router.urls)),
]
