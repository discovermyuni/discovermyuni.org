from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include
from django.urls import path
from django.views.generic import TemplateView

urlpatterns = [
    path("", TemplateView.as_view(template_name="pages/home.html", content_type="text/html"), name="home"),
    path(
        "contact/",
        TemplateView.as_view(template_name="pages/contact.html", content_type="text/html"),
        name="contact",
    ),
    path("u/", include("discovery.urls")),
    path("post/", include("posts.urls")),
    path("dashboard/", include("dashboard.urls")),
    path("myorg/", include("organizations.urls")),
    path("account/", include("allauth.urls")),
    path("users/", include("users.urls")),
    path("admin/", admin.site.urls),
]

urlpatterns += [
    path("api/posts/", include(("posts.api_urls", "posts"), namespace="posts-api")),
    path("api/users/", include(("users.api_urls", "users"), namespace="users-api")),
    path("api/discovery/", include(("discovery.api_urls", "discovery"), namespace="discovery-api")),
    path("api/organizations/", include(("organizations.api_urls", "organizations"), namespace="organizations-api")),
]

if settings.DEBUG:
    urlpatterns += static("robots.txt", document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
