from django.urls import path
from posts import views

urlpatterns = [
    path("<int:pk>/", views.PostDetailView.as_view(), name="post-detail"),
]
