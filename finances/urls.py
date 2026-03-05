from django.urls import include, path
from rest_framework.routers import DefaultRouter

from finances.views import (
    AccountViewSet,
    CategoryViewSet,
    TicketViewSet,
    TransactionViewSet,
)

router = DefaultRouter()
router.register(r"accounts", AccountViewSet, basename="accounts")
router.register(r"categorys", CategoryViewSet, basename="categorys")
router.register(r"tickets", TicketViewSet, basename="tickets")
router.register(r"transactions", TransactionViewSet, basename="transactions")

urlpatterns = [
    path("", include(router.urls)),
]
