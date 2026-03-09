from rest_framework.viewsets import ModelViewSet

from finances.models import Account, Category, Ticket, Transaction
from finances.serializers import (
    AccountSerializer,
    CategorySerializer,
    TicketSerializer,
    TransactionSerializer,
)
from tenants.mixins import TenantMixin


# UPDATE: Limitar Accounts a 3 en Free (perform_create vs serializer create)
class AccountViewSet(TenantMixin, ModelViewSet):
    lookup_field = "uid"
    serializer_class = AccountSerializer
    http_method_names = ["post", "get", "patch", "delete"]

    def get_queryset(self):
        return Account.objects.filter(tenant=self.request.tenant).distinct()

    def perform_create(self, serializer):
        tenant = self.request.tenant
        serializer.save(tenant=tenant)


# UPDATE: Limitar Categories a 10 en Free
class CategoryViewSet(TenantMixin, ModelViewSet):
    lookup_field = "uid"
    serializer_class = CategorySerializer
    http_method_names = ["post", "get", "patch", "delete"]

    def get_queryset(self):
        return Category.objects.filter(tenant=self.request.tenant).distinct()

    def perform_create(self, serializer):
        tenant = self.request.tenant
        serializer.save(tenant=tenant)


# UPDATE: Tickets solo para Paid
class TicketViewSet(TenantMixin, ModelViewSet):
    lookup_field = "uid"
    serializer_class = TicketSerializer
    http_method_names = ["post", "get", "patch", "delete"]

    def get_queryset(self):
        return Ticket.objects.filter(tenant=self.request.tenant).distinct()

    def perform_create(self, serializer):
        tenant = self.request.tenant
        serializer.save(tenant=tenant)


class TransactionViewSet(TenantMixin, ModelViewSet):
    lookup_field = "uid"
    serializer_class = TransactionSerializer
    http_method_names = ["post", "get", "patch", "delete"]

    def get_queryset(self):
        return Transaction.objects.filter(tenant=self.request.tenant).distinct()

    def perform_create(self, serializer):
        tenant = self.request.tenant
        serializer.save(tenant=tenant)
