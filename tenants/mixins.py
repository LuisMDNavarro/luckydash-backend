from tenants.constants import SUBSCRIPTION_LIMITS
from tenants.models import Membership


class TenantMixin:
    def initial(self, request, *args, **kwargs):
        super().initial(request, *args, **kwargs)

        if request.user.is_authenticated:
            tenant = getattr(request, "tenant", None)
            if tenant:
                membership = Membership.objects.filter(
                    user=request.user, tenant=request.tenant
                ).first()
                if membership:
                    request.tenant = membership.tenant
                    request.role = membership.role
                    request.limits = SUBSCRIPTION_LIMITS[
                        membership.tenant.subscription_type
                    ]
                else:
                    request.tenant = None
                    request.role = None
            else:
                membership = Membership.objects.filter(user=request.user).first()
                if membership:
                    request.tenant = membership.tenant
                    request.role = membership.role
                    request.limits = SUBSCRIPTION_LIMITS[
                        membership.tenant.subscription_type
                    ]
                else:
                    request.tenant = None
                    request.role = None
        else:
            request.tenant = None
            request.role = None
