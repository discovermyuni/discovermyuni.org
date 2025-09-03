from django.urls import path

from . import views

app_name = "organizations"
urlpatterns = [
    path("", views.manage_organizations, name="manage-organizations"),
    path("<slug:organization_slug>/", views.manage_organization_details, name="organization-details"),
    path("<slug:organization_slug>/requests/", views.manage_organization_requests, name="organization-requests"),
]
