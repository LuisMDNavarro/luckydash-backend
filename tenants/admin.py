from django.contrib import admin

from tenants.models import Membership, Tenant

admin.site.register(Tenant)
admin.site.register(Membership)
