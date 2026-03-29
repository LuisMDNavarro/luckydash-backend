from django.urls import include, path
from rest_framework.routers import DefaultRouter

from users.views import (
    CookieTokenRefreshView,
    CustomUserViewSet,
    LoginView,
    RegisterView,
)

router = DefaultRouter()
router.register(r"", CustomUserViewSet, basename="users")

urlpatterns = [
    path("register/", RegisterView.as_view(), name="register"),
    path("login/", LoginView.as_view(), name="token_obtain_pair"),
    path("refresh/", CookieTokenRefreshView.as_view(), name="token_refresh"),
    path("", include(router.urls)),
]
