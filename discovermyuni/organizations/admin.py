from django.contrib import admin

from .models import Organization
from .models import OrganizationProfile
from .models import OrganizationRequest

admin.site.register(Organization)
admin.site.register(OrganizationProfile)
admin.site.register(OrganizationRequest)

