from django.contrib import admin
from django.urls import include
from django.urls import path
from django.views.generic import TemplateView

urlpatterns = [
    path("", TemplateView.as_view(template_name="pages/home.html"), name="home"),
    path("about/", TemplateView.as_view(template_name="pages/about.html"), name="about"),
    path("account/", include("allauth.urls")),
    path("users/", include("users.urls")),
    path("posts/", include("posts.urls.pages")),
    path("post/", include("posts.urls.detail")),
    path("dashboard/", include("dashboard.urls")),
    path("admin/", admin.site.urls),
    path("api/posts/", include("posts.urls.api")),
    path(
        "robots.txt",
        TemplateView.as_view(template_name="robots.txt", content_type="text/plain"),
    ),
]
