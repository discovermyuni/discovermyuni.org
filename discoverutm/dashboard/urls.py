from django.urls import path

from . import views

app_name = "dashboard"
urlpatterns = [
    path("", views.dashboard_page_view, name="home"),
    path("new/", views.post_form_view, name="new-post"),
    path("edit/<int:pk>/", views.post_edit_view, name="edit-post"),
    path("new-template/", views.post_template_form_view, name="new-template"),
]
