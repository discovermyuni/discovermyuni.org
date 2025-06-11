from common.serializers import OrganizationSerializer
from django.contrib.auth import get_user_model
from rest_framework import serializers

from .models import Profile

User = get_user_model()


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ["id", "name", "email", "global_background", "is_staff"]
        read_only_fields = ["id", "is_staff"]


class ProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    organization = OrganizationSerializer(read_only=True)

    class Meta:
        model = Profile
        fields = ["id", "local_background", "organization", "user"]
        read_only_fields = ["id", "user", "organization"]
