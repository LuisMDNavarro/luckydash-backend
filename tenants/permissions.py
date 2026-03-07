from rest_framework.permissions import BasePermission

from tenants.constants import (
    EDIT_ACTIONS,
    EDIT_ROLES,
    OWNER_ROLE,
    READ_ACTIONS,
    READ_ROLES,
)
from tenants.models import Membership


class TenantRequired(BasePermission):
    def has_permission(self, request, view):
        return hasattr(request, "tenant") and request.tenant is not None


class TenantRole(BasePermission):
    def has_permission(self, request, view):
        if view.action in EDIT_ACTIONS:
            return hasattr(request, "role") and request.role in EDIT_ROLES
        if view.action in READ_ACTIONS:
            return hasattr(request, "role") and request.role in READ_ROLES


class AdminTenantOnly(BasePermission):
    def has_object_permission(self, request, view, obj):
        if view.action in ["destroy"]:
            membership = Membership.objects.filter(
                tenant=obj, user=request.user
            ).first()
            return membership.role == OWNER_ROLE
        elif view.action != "retrieve":
            membership = Membership.objects.filter(
                tenant=obj, user=request.user
            ).first()
            return membership.role in EDIT_ROLES
        else:
            return True


class EditMembership(BasePermission):
    def has_permission(self, request, view):
        if view.action in ["create"]:
            return hasattr(request, "role") and request.role in EDIT_ROLES
        if view.action in READ_ACTIONS:
            return hasattr(request, "role") and request.role in READ_ROLES
        if view.action in ["update", "partial_update", "destroy"]:
            return True

    def has_object_permission(self, request, view, obj):
        if view.action in ["destroy"]:
            if obj.user == request.user:
                if request.role == OWNER_ROLE:
                    return False
                else:
                    return True
            elif obj.role in EDIT_ROLES:
                return False
            else:
                return request.role in EDIT_ROLES
        elif view.action in ["update", "partial_update"]:
            return request.role == OWNER_ROLE
        else:
            return True
