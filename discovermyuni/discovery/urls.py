from django.urls import path

from . import views

app_name = "discovery"
urlpatterns = [
    path("", views.browse_organizations, name="browse_organizations"),
    path("<slug:slug>/", views.organization_posts, name="organization_posts"),
]
