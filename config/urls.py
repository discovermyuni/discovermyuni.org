from django.contrib import admin
from django.urls import include
from django.urls import path

urlpatterns = [
    path("", include("posts.urls")),
    path("api/posts/", include("posts.api_urls")),
    path("admin/", admin.site.urls),
    path("accounts/", include("allauth.urls")),
]
