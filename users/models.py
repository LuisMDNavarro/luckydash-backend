from django.contrib.auth.models import AbstractUser
from django.db import models

from luckydash.models import UIDField


class CustomUser(AbstractUser):
    uid = UIDField(prefix="user")
    tenants = models.ManyToManyField("tenants.Tenant", through="tenants.Membership")

    def __str__(self):
        return super().__str__() + f"-[{self.uid}]"
