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


class SwitchTenantView(TenantMixin, APIView):
    def post(self, request):
        membership_uid = request.data.get("membership_uid")
        if membership_uid:
            try:
                user = self.request.user
                membership = Membership.objects.get(uid=membership_uid, user=user)
                request.session["membership_uid"] = membership.uid
                return Response(
                    {
                        "message": "Cambio exitoso",
                    },
                    status=HTTP_200_OK,
                )
            except Membership.DoesNotExist:
                return Response(
                    {
                        "error": "La cartera no existe",
                    },
                    status=HTTP_404_NOT_FOUND,
                )
        return Response(
            {
                "error": "Se debe seleccionar una cartera",
            },
            status=HTTP_404_NOT_FOUND,
        )
