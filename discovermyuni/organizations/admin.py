from django.contrib import admin

from .models import Organization
from .models import OrganizationRequest

admin.site.register(Organization)
admin.site.register(OrganizationRequest)
