from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

from finances.constans import (
    ACCOUNT_TYPES,
    CATEGORY_TYPES,
    DEFAULT_ACCOUNT_TYPE,
    DEFAULT_CATEGORY_TYPE,
    DEFAULT_TRANSACTION_TYPE,
    TRANSACTION_TYPES,
)
from finances.utils import hex_color_validator
from luckydash.models import BaseModel, UIDField
from tenants.models import Tenant


class Account(BaseModel):
    uid = UIDField(prefix="account")
    tenant = models.ForeignKey(Tenant, on_delete=models.CASCADE)
    name = models.CharField(max_length=255, null=False)
    color = models.CharField(max_length=7, validators=[hex_color_validator])
    type = models.CharField(
        max_length=255, choices=ACCOUNT_TYPES, default=DEFAULT_ACCOUNT_TYPE
    )
    # Cash or Debit
    savings = models.DecimalField(
        max_digits=12, decimal_places=2, null=True, blank=True
    )
    amount = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
    # Credit
    credit_limit = models.DecimalField(
        max_digits=12, decimal_places=2, null=True, blank=True
    )
    billing_date = models.IntegerField(
        null=True, blank=True, validators=[MinValueValidator(1), MaxValueValidator(31)]
    )
    payment_deadline = models.IntegerField(
        null=True, blank=True, validators=[MinValueValidator(1), MaxValueValidator(31)]
    )

    def __str__(self):
        return super().__str__() + f"-[{self.name}]"


class Category(BaseModel):
    uid = UIDField(prefix="category")
    tenant = models.ForeignKey(Tenant, on_delete=models.CASCADE)
    name = models.CharField(max_length=255, null=False)
    color = models.CharField(max_length=7, validators=[hex_color_validator])
    type = models.CharField(
        max_length=255, choices=CATEGORY_TYPES, default=DEFAULT_CATEGORY_TYPE
    )

    def __str__(self):
        return super().__str__() + f"-[{self.name}]"


class Ticket(BaseModel):
    uid = UIDField(prefix="ticket")
    tenant = models.ForeignKey(Tenant, on_delete=models.CASCADE)
    account = models.ForeignKey(Account, on_delete=models.PROTECT)
    total_amount = models.DecimalField(max_digits=12, decimal_places=2, null=False)
    description = models.CharField(max_length=255, null=False)
    purchase_date = models.DateTimeField(null=False)
    approval_date = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return super().__str__() + f"-[{self.description}]"


class Transaction(BaseModel):
    uid = UIDField(prefix="transaction")
    tenant = models.ForeignKey(Tenant, on_delete=models.CASCADE)
    ticket = models.ForeignKey(Ticket, on_delete=models.SET_NULL, null=True, blank=True)
    from_account = models.ForeignKey(
        Account, on_delete=models.PROTECT, related_name="outgoing_transactions"
    )
    category = models.ForeignKey(Category, on_delete=models.PROTECT)
    type = models.CharField(
        max_length=255, choices=TRANSACTION_TYPES, default=DEFAULT_TRANSACTION_TYPE
    )
    amount = models.DecimalField(max_digits=12, decimal_places=2, null=False)
    description = models.CharField(max_length=255, null=False)
    purchase_date = models.DateTimeField(null=False)
    # Expense on installments
    installments = models.PositiveSmallIntegerField(null=True, blank=True)
    installment_number = models.PositiveSmallIntegerField(null=True, blank=True)
    parent_transaction = models.ForeignKey(
        "self",
        null=True,
        blank=True,
        on_delete=models.CASCADE,
        related_name="installment_transactions",
    )
    # Credit expense
    approval_date = models.DateTimeField(null=True, blank=True)
    # Intern transfer
    to_account = models.ForeignKey(
        Account,
        on_delete=models.PROTECT,
        related_name="incoming_transactions",
        null=True,
        blank=True,
    )
    # Monthly expense
    is_monthly = models.BooleanField(default=False)

    def __str__(self):
        return super().__str__() + f"-[{self.description}]"
