from rest_framework.serializers import ModelSerializer

from tenants.models import Tenant


class TenantSerializer(ModelSerializer):
    class Meta:
        model = Tenant
        fields = ["uid", "name", "subscription_type"]
