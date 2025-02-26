from django.contrib.auth import get_user_model
from rest_framework import serializers

User = get_user_model()

class ProfileSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ["id", "name", "is_author", "is_staff"]
        read_only_fields = ["is_author, is_staff"]


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ["id", "name", "email", "is_author", "is_staff"]
        read_only_fields = ["is_author, is_staff"]
