from django.contrib.auth import get_user_model
from rest_framework import serializers

from .models import Post

User = get_user_model()


class PostSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Post
        fields = ["id", "title", "description", "creator", "start_date", "end_date", "created_at", "location", "tags"]
        read_only_fields = ["is_staff", "is_superuser"]
