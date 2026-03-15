from django.db.transaction import atomic
from rest_framework.serializers import (
    CharField,
    DecimalField,
    ModelSerializer,
    Serializer,
    ValidationError,
)

from finances.constans import (
    CREDIT_TYPE,
    DEBIT_TYPE,
    DEFAULT_ACCOUNT_TYPE,
    MAX_INSTALLMENTS,
    MIN_INSTALLMENTS,
    TRANSFER_TRANSACTION_TYPE,
)
from finances.models import Account, Category, Ticket, Transaction
from luckydash.constants import ERROR_MESSAGES


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


class CategoryField(CharField):

    def to_internal_value(self, data):
        uid = super().to_internal_value(data)
        tenant = self.context["request"].tenant
        category = Category.objects.filter(uid=uid, tenant=tenant).first()
        if not category:
            raise ValidationError("La categoria no existe")
        return category


class TransactionInputSerializer(Serializer):
    category = CategoryField(error_messages=ERROR_MESSAGES)
    amount = DecimalField(max_digits=10, decimal_places=2)
    description = CharField(error_messages=ERROR_MESSAGES)


class TicketSerializer(ModelSerializer):
    account = CharField(error_messages=ERROR_MESSAGES)
    total_amount = CharField(read_only=True)
    transactions = TransactionInputSerializer(many=True, write_only=True)

    class Meta:
        model = Ticket
        fields = [
            "uid",
            "account",
            "total_amount",
            "description",
            "purchase_date",
            "approval_date",
            "transactions",
        ]

    def validate_account(self, value):
        request = self.context.get("request")
        account = Account.objects.filter(uid=value, tenant=request.tenant).first()
        if not account:
            raise ValidationError("La cuenta no existe")
        return account

    def update(self, instance, validated_data):
        if (
            validated_data.get("account")
            or validated_data.get("purchase_date")
            or validated_data.get("approval_date")
        ):
            transactions = Transaction.objects.filter(ticket=instance)
            for t in transactions:
                t.from_account = validated_data.get("account", instance.account)
                t.purchase_date = validated_data.get(
                    "purchase_date", instance.purchase_date
                )
                t.approval_date = validated_data.get(
                    "approval_date", instance.approval_date
                )
                t.save()
        transactions_data = validated_data.pop("transactions", None)
        if transactions_data:
            with atomic():
                validated_data["total_amount"] = instance.total_amount + sum(
                    t["amount"] for t in transactions_data
                )
                for transaction in transactions_data:
                    Transaction.objects.create(
                        tenant=self.context["request"].tenant,
                        from_account=validated_data.get("account", instance.account),
                        purchase_date=validated_data.get(
                            "purchase_date", instance.purchase_date
                        ),
                        approval_date=validated_data.get(
                            "approval_date", instance.approval_date
                        ),
                        ticket=instance,
                        **transaction,
                    )
        return super().update(instance, validated_data)

    def create(self, validated_data):
        with atomic():
            transactions_data = validated_data.pop("transactions")
            validated_data["total_amount"] = sum(t["amount"] for t in transactions_data)
            ticket = Ticket.objects.create(**validated_data)
            for transaction in transactions_data:
                Transaction.objects.create(
                    tenant=self.context["request"].tenant,
                    from_account=validated_data["account"],
                    purchase_date=validated_data["purchase_date"],
                    approval_date=validated_data.get("approval_date"),
                    ticket=ticket,
                    **transaction,
                )
        return ticket


class TransactionSerializer(ModelSerializer):
    from_account = CharField(error_messages=ERROR_MESSAGES)
    category = CharField(error_messages=ERROR_MESSAGES)
    ticket = CharField(read_only=True)
    to_account = CharField(required=False, error_messages=ERROR_MESSAGES)
    parent_transaction = CharField(read_only=True)
    installment_number = CharField(read_only=True)

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

    def validate_from_account(self, value):
        request = self.context.get("request")
        account = Account.objects.filter(uid=value, tenant=request.tenant).first()
        if not account:
            raise ValidationError("La cuenta no existe")
        return account

    def validate_category(self, value):
        request = self.context.get("request")
        category = Category.objects.filter(uid=value, tenant=request.tenant).first()
        if not category:
            raise ValidationError("La categoria no existe")
        return category

    def validate_installments(self, value):
        if value < MIN_INSTALLMENTS:
            raise ValidationError(f"El minimo de cuotas es: {MIN_INSTALLMENTS}")
        if value > MAX_INSTALLMENTS:
            raise ValidationError(f"Excede el maximo de cuotas: {MAX_INSTALLMENTS}")
        return value

    def validate_to_account(self, value):
        request = self.context.get("request")
        account = Account.objects.filter(uid=value, tenant=request.tenant).first()
        if not account:
            raise ValidationError("La cuenta no existe")
        return account

    def validate(self, data):
        if data.get("type") == TRANSFER_TRANSACTION_TYPE:
            data.pop("installments", None)
            to_account = data.get("to_account")
            if to_account is not None and data.get("from_account") == to_account:
                raise ValidationError(
                    "La cuenta destino no puede ser la misma que la cuenta origen."
                )
        else:
            data.pop("to_account", None)
        return data

    def update(self, instance, validated_data):
        if (
            instance.installments
            or instance.parent_transaction
            or instance.installment_number
        ):
            raise ValidationError("No puedes modificar las Transacciones a cuotas")
        if validated_data.get("type") != TRANSFER_TRANSACTION_TYPE:
            instance.to_account = None
        if instance.ticket:
            validated_data["from_account"] = instance.from_account
            validated_data["purchase_date"] = instance.purchase_date
            validated_data["approval_date"] = instance.approval_date
            if instance.amount != validated_data["amount"]:
                ticket = instance.ticket
                ticket.total_amount = ticket.total_amount + (
                    validated_data["amount"] - instance.amount
                )
                ticket.save()
        return super().update(instance, validated_data)

    def create(self, validated_data):
        installments = validated_data.get("installments")
        if installments:
            with atomic():
                partial_amount = validated_data.get("amount") / installments
                validated_data["amount"] = partial_amount
                validated_data["installment_number"] = 1
                transaction = Transaction.objects.create(**validated_data)
                validated_data["parent_transaction"] = transaction
                for i in range(MIN_INSTALLMENTS, installments + 1):
                    validated_data["installment_number"] = i
                    Transaction.objects.create(**validated_data)
        else:
            transaction = Transaction.objects.create(**validated_data)
        return transaction
