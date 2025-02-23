from django.contrib.auth import get_user_model
from rest_framework import serializers

User = get_user_model()


# TODO: add API view w/ authentication, users can fetch any other users

class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ["id", "email", "name", "is_staff", "is_superuser"]
        read_only_fields = ["is_staff", "is_superuser"]
