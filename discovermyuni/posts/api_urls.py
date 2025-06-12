from django.urls import path
from posts import views

urlpatterns = [
    path("fetch/", views.fetch_posts, name="fetch-posts"),
    path("render-cards/", views.render_cards, name="render-cards"),
    path("bot-publish", views.render_cards),
]
