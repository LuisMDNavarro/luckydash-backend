from rest_framework.serializers import ModelSerializer

from finances.models import Account, Category, Ticket, Transaction


class AccountSerializer(ModelSerializer):
    class Meta:
        model = Account
        fields = [
            "uid",
            "tenant",
            "name",
            "color",
            "type",
            "savings",
            "amount",
            "credit_limit",
            "billing_date",
            "payment_deadline",
        ]


class CategorySerializer(ModelSerializer):
    class Meta:
        model = Category
        fields = ["uid", "tenant", "name", "color", "type"]


class TicketSerializer(ModelSerializer):
    class Meta:
        model = Ticket
        fields = [
            "uid",
            "tenant",
            "account",
            "total_amount",
            "description",
            "purchase_date",
            "approval_date",
        ]


class TransactionSerializer(ModelSerializer):
    class Meta:
        model = Transaction
        fields = [
            "uid",
            "tenant",
            "ticket",
            "from_account",
            "category",
            "type",
            "amount",
            "description",
            "purchase_date",
            "installments",
            "installment_number",
            "parent_transaction",
            "approval_date",
            "to_account",
            "is_monthly",
        ]
