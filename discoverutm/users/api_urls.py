from django.urls import path

from . import views

urlpatterns = [
    path(
        "profile/<slug:organization_slug>/<str:username>/",
        views.profile_api_view,
        name="get-profile-api",
    ),
]
