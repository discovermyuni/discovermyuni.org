from django.contrib.auth import get_user_model
from rest_framework import serializers

from .models import Post

User = get_user_model()


class PostSerializer(serializers.HyperlinkedModelSerializer):
    author = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())
    tags = serializers.SerializerMethodField()

    class Meta:
        model = Post
        fields = [
            "id", "title", "description", "author", "start_date", "end_date",
            "created_at", "location", "tags", "image_url",
        ]
        read_only_fields = ["is_staff", "is_superuser"]

    def get_tags(self, obj):
        return list(obj.tags.values_list("name", flat=True))

    def create(self, validated_data):
        tags_data = validated_data.pop("tags", [])

        post = Post.objects.create(**validated_data)
        post.tags.add(*tags_data)

        return post
