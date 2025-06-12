from django.urls import path

from . import views

app_name = "organizations"
urlpatterns = [
    path("", views.manage_organizations, name="manage-organizations"),
]
