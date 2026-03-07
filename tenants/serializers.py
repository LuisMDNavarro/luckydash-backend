from rest_framework.serializers import CharField, ModelSerializer, ValidationError

from luckydash.constants import ERROR_MESSAGES
from tenants.models import Membership, Tenant
from users.models import CustomUser


class TenantSerializer(ModelSerializer):
    subscription_type = CharField(read_only=True)

    class Meta:
        model = Tenant
        fields = ["uid", "name", "subscription_type"]


class MembershipSerializer(ModelSerializer):
    user = CharField(error_messages=ERROR_MESSAGES)

    class Meta:
        model = Membership
        fields = ["uid", "user", "role"]

    def validate_user(self, value):
        user = CustomUser.objects.filter(username=value).first()
        if not user:
            raise ValidationError({"user": "El usuario no existe"})
        return user
