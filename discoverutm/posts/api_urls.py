from django.urls import path

from .views import create_post
from .views import get_posts

app_name = "posts_api"
urlpatterns = [
    path("get", get_posts, name="get_posts"),
    path("create", create_post, name="create_post"),
]
