from tenants.constants import SUBSCRIPTION_LIMITS
from tenants.models import Membership


class TenantMixin:
    def initial(self, request, *args, **kwargs):
        super().initial(request, *args, **kwargs)

        if request.user.is_authenticated:
            membership_uid = request.session.get("membership_uid")
            if membership_uid:
                membership = Membership.objects.filter(
                    uid=membership_uid, user=request.user
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
