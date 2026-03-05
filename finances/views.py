from rest_framework.viewsets import ModelViewSet

from finances.models import Account, Category, Ticket, Transaction
from finances.serializers import (
    AccountSerializer,
    CategorySerializer,
    TicketSerializer,
    TransactionSerializer,
)
from tenants.mixins import TenantMixin


# UPDATE: Aplicar Permissions de Tenant y Admin a todo
class AccountViewSet(TenantMixin, ModelViewSet):
    lookup_field = "uid"
    serializer_class = AccountSerializer
    http_method_names = ["post", "get", "patch", "delete"]

    def get_queryset(self):
        return Account.objects.filter(tenant=self.request.tenant).distinct()


class CategoryViewSet(TenantMixin, ModelViewSet):
    lookup_field = "uid"
    serializer_class = CategorySerializer
    http_method_names = ["post", "get", "patch", "delete"]

    def get_queryset(self):
        return Category.objects.filter(tenant=self.request.tenant).distinct()


class TicketViewSet(TenantMixin, ModelViewSet):
    lookup_field = "uid"
    serializer_class = TicketSerializer
    http_method_names = ["post", "get", "patch", "delete"]

    def get_queryset(self):
        return Ticket.objects.filter(tenant=self.request.tenant).distinct()


class TransactionViewSet(TenantMixin, ModelViewSet):
    lookup_field = "uid"
    serializer_class = TransactionSerializer
    http_method_names = ["post", "get", "patch", "delete"]

    def get_queryset(self):
        return Transaction.objects.filter(tenant=self.request.tenant).distinct()
