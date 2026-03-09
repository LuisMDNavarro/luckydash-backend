from rest_framework.serializers import ModelSerializer, ValidationError

from finances.constans import CREDIT_TYPE, DEBIT_TYPE, DEFAULT_ACCOUNT_TYPE
from finances.models import Account, Category, Ticket, Transaction


class AccountSerializer(ModelSerializer):
    class Meta:
        model = Account
        fields = [
            "uid",
            "name",
            "color",
            "type",
            "savings",
            "amount",
            "credit_limit",
            "billing_date",
            "payment_deadline",
        ]

    def validate(self, data):
        if not data.get("type"):
            data["type"] = DEFAULT_ACCOUNT_TYPE
        if data["type"] in [DEFAULT_ACCOUNT_TYPE, DEBIT_TYPE]:
            data.pop("credit_limit", None)
            data.pop("billing_date", None)
            data.pop("payment_deadline", None)
        if data["type"] in [CREDIT_TYPE]:
            data.pop("savings", None)
            data.pop("amount", None)
            if not data.get("credit_limit"):
                raise ValidationError({"credit_limit": "Este campo es obligatorio."})
            if not data.get("billing_date"):
                raise ValidationError({"billing_date": "Este campo es obligatorio."})
            if not data.get("payment_deadline"):
                raise ValidationError(
                    {"payment_deadline": "Este campo es obligatorio."}
                )
        return data

    def update(self, instance, validated_data):
        if validated_data["type"] in [DEFAULT_ACCOUNT_TYPE, DEBIT_TYPE]:
            instance.credit_limit = None
            instance.billing_date = None
            instance.payment_deadline = None
        if validated_data["type"] in [CREDIT_TYPE]:
            instance.savings = None
            instance.amount = None
        return super().update(instance, validated_data)


class CategorySerializer(ModelSerializer):
    class Meta:
        model = Category
        fields = ["uid", "name", "color", "type"]


# UPDATE: Validar foreing_keys a Tickets y Transactions
class TicketSerializer(ModelSerializer):
    class Meta:
        model = Ticket
        fields = [
            "uid",
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
