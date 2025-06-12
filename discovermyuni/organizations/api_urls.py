from django.urls import path

from . import views

urlpatterns = [
    path(
        "apply-organization/<int:organization_id>",
        views.apply_to_organization,
        name="apply-to-organization",
    ),
]
