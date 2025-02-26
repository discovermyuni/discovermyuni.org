from django.urls import path

from . import views

app_name = "posts"
urlpatterns = [
    path("posts/", views.home_page_view, name="home"),
    path("posts/d/new", views.post_form_view, name="new"),
    path("post/<int:pk>", views.PostDetailView.as_view(), name="post-detail"),
]
