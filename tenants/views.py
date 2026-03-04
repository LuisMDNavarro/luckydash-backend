from django.db.transaction import atomic
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK, HTTP_404_NOT_FOUND
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet

from tenants.constants import OWNER_ROLE
from tenants.mixins import TenantMixin
from tenants.models import Membership, Tenant
from tenants.serializers import TenantSerializer


class TenantViewSet(ModelViewSet):
    lookup_field = "uid"
    serializer_class = TenantSerializer
    http_method_names = ["post", "get", "patch", "delete"]

    def get_queryset(self):
        user = self.request.user
        return Tenant.objects.filter(membership__user=user).distinct()

    def perform_create(self, serializer):
        with atomic():
            tenant = serializer.save()
            user = self.request.user
            Membership.objects.create(
                tenant=tenant,
                user=user,
                role=OWNER_ROLE,
            )


# UPDATE: Terminar endpoint de cambio de Tenant
class SwitchTenantView(TenantMixin, APIView):
    def post(self, request):
        tenant_uid = request.data.get("tenant_uid")
        if tenant_uid:
            try:
                user = self.request.user
                tenant = Tenant.objects.get(uid=tenant_uid, membership__user=user)
                request.tenant = tenant
                return Response(
                    {
                        "message": "Cambio exitoso",
                    },
                    status=HTTP_200_OK,
                )
            except Tenant.DoesNotExist:
                return Response(
                    {
                        "error": "La cartera no existe",
                    },
                    status=HTTP_404_NOT_FOUND,
                )
        return Response(
            {
                "error": "La cartera no existe",
            },
            status=HTTP_404_NOT_FOUND,
        )
