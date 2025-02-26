from django.contrib import admin
from django.urls import include
from django.urls import path
from django.views.generic import TemplateView
from django.shortcuts import redirect

urlpatterns = [
    path("", TemplateView.as_view(template_name="pages/home.html"), name="home"),
    path("", include("posts.urls")),
    path("about/", TemplateView.as_view(template_name="pages/about.html"), name="about"),
    path("admin/", admin.site.urls),
    path("accounts/", include("allauth.urls")),
    path("users/", include("users.urls")),
    path("api/posts/", include("posts.api_urls")),
    path("login/", lambda request: redirect("account_login")),  # Redirect to Allauth login
]
