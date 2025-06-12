from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.db.models import QuerySet
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from django.views.generic import DetailView
from django.views.generic import RedirectView
from django.views.generic import UpdateView
from organizations.models import Organization
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Profile
from .serializers import ProfileSerializer

User = get_user_model()


class UserDetailView(LoginRequiredMixin, DetailView):
    model = User
    slug_field = "id"
    slug_url_kwarg = "id"


user_detail_view = UserDetailView.as_view()


class UserUpdateView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = User
    fields = ["name"]
    success_message = _("Information successfully updated")

    def get_success_url(self) -> str:
        assert self.request.user.is_authenticated  # type guard
        return self.request.user.get_absolute_url()

    def get_object(self, queryset: QuerySet | None = None) -> User:
        assert self.request.user.is_authenticated  # type guard
        return self.request.user


user_update_view = UserUpdateView.as_view()


class UserRedirectView(LoginRequiredMixin, RedirectView):
    permanent = False

    def get_redirect_url(self) -> str:
        return reverse("users:detail", kwargs={"pk": self.request.user.pk})


user_redirect_view = UserRedirectView.as_view()


class ProfileAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, organization_slug, username):
        try:
            organization = Organization.objects.get(slug=organization_slug)
            user = User.objects.get(username=username)
        except Organization.DoesNotExist:
            return Response({"error": "Organization not found"}, status=404)
        except User.DoesNotExist:
            return Response({"error": "User not found"}, status=404)

        profile = Profile.objects.filter(organization=organization, user=user).first()
        if not profile.exists():
            return Response({"error": "Profile not found"}, status=404)

        serializer = ProfileSerializer(profile.first())
        return Response(serializer.data)


profile_api_view = ProfileAPIView.as_view()
