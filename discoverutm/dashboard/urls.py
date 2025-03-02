from django.urls import path

from . import views

app_name = "dashboard"
urlpatterns = [
    path("", views.dashboard_page_view, name="home"),
    path("new/", views.post_form_view, name="new-post"),
]
