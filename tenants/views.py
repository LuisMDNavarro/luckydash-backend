from django.db.transaction import atomic
from django.utils import timezone
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK, HTTP_404_NOT_FOUND
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet

from tenants.constants import OWNER_ROLE
from tenants.mixins import TenantMixin
from tenants.models import Membership, Tenant
from tenants.permissions import AdminTenantOnly, EditMembership, TenantRequired
from tenants.serializers import MembershipSerializer, TenantSerializer


# UPDATE: Solo un Tenant para Free,
# debe tener al menos un Tenan que cumpla rol = owner y sub_type = paid
class TenantViewSet(TenantMixin, ModelViewSet):
    permission_classes = [IsAuthenticated, AdminTenantOnly]
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


class SwitchTenantView(TenantMixin, APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        tenant_uid = request.data.get("tenant_uid")
        if tenant_uid:
            try:
                user = self.request.user
                membership = Membership.objects.get(tenant__uid=tenant_uid, user=user)
                request.session["membership_uid"] = membership.uid
                return Response(
                    {
                        "tenant_uid": tenant_uid,
                    },
                    status=HTTP_200_OK,
                )
            except Membership.DoesNotExist:
                return Response(
                    {
                        "error": {
                            "tenant_uid": "La cartera no existe",
                        }
                    },
                    status=HTTP_404_NOT_FOUND,
                )
        return Response(
            {
                "error": {
                    "tenant_uid": "Este campo es obligatorio.",
                }
            },
            status=HTTP_404_NOT_FOUND,
        )


# UPDATE: Solo 3 membresias por Tenant en free
class MembershipViewSet(TenantMixin, ModelViewSet):
    permission_classes = [IsAuthenticated, TenantRequired, EditMembership]
    lookup_field = "uid"
    serializer_class = MembershipSerializer
    http_method_names = ["post", "get", "patch", "delete"]

    def get_queryset(self):
        tenant = self.request.tenant
        return Membership.objects.filter(tenant=tenant).distinct()

    def perform_create(self, serializer):
        tenant = self.request.tenant
        user = serializer.validated_data.get("user")
        role = serializer.validated_data.get("role")
        membership = Membership.raw_objects.filter(user=user, tenant=tenant).first()
        if membership:
            membership.deleted_at = None
            membership.updated_at = timezone.now()
            if role:
                membership.role = role
            membership.save()
        else:
            serializer.save(tenant=tenant)
