from django.urls import path

from . import views

app_name = "discovery"
urlpatterns = [
    path("", views.discovery_home, name="home"),
    path("<slug:slug>/", views.organization_posts, name="organization_posts"),
]
