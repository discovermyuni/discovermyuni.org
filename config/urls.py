from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include
from django.urls import path
from django.views.generic import TemplateView

urlpatterns = [
    path("", include("posts.urls.pages")),
    path("account/", include("allauth.urls")),
    path("users/", include("users.urls")),
    path("post/", include("posts.urls.detail")),
    path("dashboard/", include("dashboard.urls")),
    path("admin/", admin.site.urls),
    path("api/posts/", include("posts.urls.api")),
    path(
        "robots.txt",
        TemplateView.as_view(template_name="robots.txt", content_type="text/plain"),
    ),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
