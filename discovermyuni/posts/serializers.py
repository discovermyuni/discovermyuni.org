from django.contrib.auth import get_user_model
from rest_framework import serializers

from .models import Post

User = get_user_model()


class PostSerializer(serializers.ModelSerializer):
    tags = serializers.SerializerMethodField()

    class Meta:
        model = Post
        fields = [
            "id",
            "title",
            "description",
            "author",
            "start_date",
            "end_date",
            "created_at",
            "location",
            "tags",
            "image",
            "is_generated",
        ]
        read_only_fields = ["id", "author", "is_generated", "created_at"]

    def get_tags(self, obj):
        return list(obj.tags.values_list("name", flat=True))

    def create(self, validated_data):
        validated_data["author"] = self.context["request"].user
        tags_data = validated_data.pop("tags", [])

        post = Post.objects.create(**validated_data)
        post.tags.add(*tags_data)

        return post
