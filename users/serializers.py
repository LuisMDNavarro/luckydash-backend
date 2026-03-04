from django.contrib.auth.password_validation import validate_password
from django.db.transaction import atomic
from rest_framework.serializers import CharField, ModelSerializer, ValidationError

from luckydash.constants import ERROR_MESSAGES
from tenants.constants import OWNER_ROLE
from tenants.models import Membership, Tenant
from users.models import CustomUser


class CustomUserSerializer(ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ["uid", "username", "email", "first_name", "last_name"]


class RegisterSerializer(ModelSerializer):
    password = CharField(write_only=True, error_messages=ERROR_MESSAGES)
    confirm_password = CharField(write_only=True, error_messages=ERROR_MESSAGES)
    wallet_name = CharField(error_messages=ERROR_MESSAGES)

    class Meta:
        model = CustomUser
        fields = ["username", "password", "confirm_password", "wallet_name"]

    def validate_password(self, value):
        validate_password(value)
        return value

    def validate(self, data):
        if data["password"] != data["confirm_password"]:
            raise ValidationError({"password": "Las contraseñas no coinciden."})
        return data

    def create(self, validated_data):
        validated_data.pop("confirm_password")
        tenant_name = validated_data.pop("wallet_name")
        with atomic():
            user = CustomUser.objects.create_user(**validated_data)
            tenant = Tenant.objects.create(name=tenant_name)
            Membership.objects.create(tenant=tenant, user=user, role=OWNER_ROLE)
        return user
