from django.urls import path

from . import views

urlpatterns = [
    path("apply/<int:organization_id>/", views.apply_to_organization, name="apply_to_organization-api"),
]
