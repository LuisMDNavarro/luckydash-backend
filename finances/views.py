from rest_framework.exceptions import ValidationError
from rest_framework.viewsets import ModelViewSet

from finances.constans import (
    CREDIT_TYPE,
    DEFAULT_TRANSACTION_TYPE,
    EXPENSE_SAVINGS_TRANSACTION_TYPE,
    INCOME_SAVINGS_TRANSACTION_TYPE,
    INCOME_TRANSACTION_TYPE,
    INSTALLMENTS_TRANSACTION_TYPE,
    TRANSFER_TRANSACTION_TYPE,
)
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

    def perform_destroy(self, instance):
        account = instance.account
        # Undo change in account
        if account.type == CREDIT_TYPE:
            account.credit_available = account.credit_available + instance.total_amount
        else:
            account.amount = account.amount + instance.total_amount
        account.save()

        return super().perform_destroy(instance)


class TransactionViewSet(TenantMixin, ModelViewSet):
    lookup_field = "uid"
    serializer_class = TransactionSerializer
    http_method_names = ["post", "get", "patch", "delete"]

    def get_queryset(self):
        return Transaction.objects.filter(tenant=self.request.tenant).distinct()

    def perform_create(self, serializer):
        tenant = self.request.tenant
        serializer.save(tenant=tenant)

    def perform_destroy(self, instance):
        if instance.ticket:
            ticket = instance.ticket
            ticket.total_amount -= instance.amount
            ticket.save()

        if instance.parent_transaction is not None:
            raise ValidationError(
                {"error": "No puedes borrar una cuota de una Transaccion a cuotas"}
            )
        from_account = instance.from_account
        # Undo change in from_account
        if from_account.type == CREDIT_TYPE:
            if instance.type == INSTALLMENTS_TRANSACTION_TYPE:
                total_amount = instance.amount
                installments = Transaction.objects.filter(parent_transaction=instance)
                for i in installments:
                    total_amount += i.amount
                from_account.credit_available = (
                    from_account.credit_available + total_amount
                )
            if instance.type in [DEFAULT_TRANSACTION_TYPE, TRANSFER_TRANSACTION_TYPE]:
                from_account.credit_available = (
                    from_account.credit_available + instance.amount
                )
            if instance.type == INCOME_TRANSACTION_TYPE:
                from_account.credit_available = (
                    from_account.credit_available - instance.amount
                )
        else:
            if instance.type in [DEFAULT_TRANSACTION_TYPE, TRANSFER_TRANSACTION_TYPE]:
                from_account.amount = from_account.amount + instance.amount
            if instance.type == INCOME_TRANSACTION_TYPE:
                from_account.amount = from_account.amount - instance.amount
            if instance.type == EXPENSE_SAVINGS_TRANSACTION_TYPE:
                from_account.savings = from_account.savings + instance.amount
            if instance.type == INCOME_SAVINGS_TRANSACTION_TYPE:
                from_account.savings = from_account.savings - instance.amount

        from_account.save()

        to_account = instance.to_account
        # Undo change in to_account
        if instance.type == TRANSFER_TRANSACTION_TYPE:
            if to_account.type == CREDIT_TYPE:
                to_account.credit_available = (
                    to_account.credit_available - instance.amount
                )
            else:
                to_account.amount = to_account.amount - instance.amount
            to_account.save()

        return super().perform_destroy(instance)
