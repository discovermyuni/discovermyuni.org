from typing import ClassVar

from common.models import TimeStampedModel
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.urls import reverse
from django.utils.translation import gettext_lazy as _

from .managers import UserManager


class User(AbstractUser):
    """
    Default custom user model for Discover UTM.
    If adding fields that need to be filled at user signup,
    check forms.SignupForm and forms.SocialSignupForms accordingly.
    """

    # First and last name do not cover name patterns around the globe
    name = models.CharField(_("Display Name"), max_length=255, blank=True, default="")
    first_name = None  # type: ignore[assignment]
    last_name = None  # type: ignore[assignment]
    email = models.EmailField(_("Email Address"), unique=True)
    global_background = models.TextField(_("Background"), blank=True, default="")

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username"]

    objects: ClassVar[UserManager] = UserManager()

    def save(self, *args, **kwargs):
        if not self.name and self.username:
            self.name = self.username
        super().save(*args, **kwargs)

    def get_absolute_url(self) -> str:
        """Get URL for user's detail view.

        Returns:
            str: URL for user detail.

        """
        return reverse("users:detail", kwargs={"pk": self.id})


class Profile(TimeStampedModel):
    """User profile model to store additional organization-related information."""

    organization = models.ForeignKey(
        "common.Organization",
        on_delete=models.CASCADE,
        related_name="profiles",
        verbose_name=_("Organization"),
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="profiles")
    local_background = models.TextField(_("Background"), blank=True, default="")

    class Meta:
        constraints = [models.UniqueConstraint(fields=["organization", "user"], name="unique_org_user")]

    def __str__(self):
        return f"Profile of {self.user.name} in {self.organization.name}"

    @staticmethod
    def does_profile_exist(organization, user) -> bool:
        """Check if the profile exists."""
        return Profile.objects.filter(organization=organization, user=user).exists()
