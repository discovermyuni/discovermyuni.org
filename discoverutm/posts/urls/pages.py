from django.urls import path
from posts import views

app_name = "posts"
urlpatterns = [
    path("", views.home_page_view, name="home"),
]
