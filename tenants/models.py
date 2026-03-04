from django.db import models

from luckydash.models import BaseModel, UIDField
from tenants.constants import (
    DEFAUL_SUBSCRIPTION,
    DEFAULT_ROLE,
    ROLE_CHOICES,
    SUBSCRIPTION_TYPES,
)
from users.models import CustomUser


class Tenant(BaseModel):
    uid = UIDField(prefix="tenant")
    name = models.CharField(max_length=255, null=False)
    subscription_type = models.CharField(
        max_length=20, choices=SUBSCRIPTION_TYPES, default=DEFAUL_SUBSCRIPTION
    )

    def __str__(self):
        return super().__str__() + f"-[{self.name}]"


class Membership(BaseModel):
    uid = UIDField(prefix="membership")
    tenant = models.ForeignKey(Tenant, on_delete=models.CASCADE)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default=DEFAULT_ROLE)

    class Meta:
        unique_together = ("tenant", "user")

    def __str__(self):
        return super().__str__() + f"-[{self.tenant.name} - {self.user.username}]"
