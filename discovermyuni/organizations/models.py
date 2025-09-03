import logging

from common.models import TimeStampedModel
from django.contrib.auth import get_user_model
from django.db import models
from django.urls import reverse
from django.utils.translation import gettext_lazy as _

logger = logging.getLogger(__name__)
User = get_user_model()

ORG_PERM_MANAGE = "can_manage_organization"
ORG_PERM_EDIT = "can_edit_organization"
ORG_PERM_DELETE = "can_delete_organization"
ORG_PERM_MANAGE_REQUESTS = "can_manage_organization_requests"
ORG_PERM_POST = "can_post_in_organization"


class Organization(TimeStampedModel):
    title = models.CharField(_("Title"), max_length=255)
    slug = models.CharField(_("Slug"), max_length=255, unique=True)
    description = models.TextField(_("Description"))
    background = models.TextField(_("Background"), blank=True, default="")

    # static permission variables because im an indecisive person
    PERM_MANAGE = ORG_PERM_MANAGE
    PERM_EDIT = ORG_PERM_EDIT
    PERM_DELETE = ORG_PERM_DELETE
    PERM_MANAGE_REQUESTS = ORG_PERM_MANAGE_REQUESTS
    PERM_POST = ORG_PERM_POST

    class Meta:
        permissions = [
            (ORG_PERM_MANAGE, "Can manage organization"),
            (ORG_PERM_EDIT, "Can edit organization details"),
            (ORG_PERM_DELETE, "Can delete organization"),
            (ORG_PERM_MANAGE_REQUESTS, "Can manage organization user requests"),
            (ORG_PERM_POST, "Can post in this organization"),
        ]

    def __str__(self):
        return self.title + " | " + self.slug

    def get_absolute_url(self):
        return reverse("discovery:organization_posts", args=[self.slug])


class OrganizationProfile(TimeStampedModel):
    """User profile model to store additional organization-related information."""

    organization = models.ForeignKey(
        Organization,
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
        return OrganizationProfile.objects.filter(organization=organization, user=user).exists()



class OrganizationRequest(TimeStampedModel):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="organization_requests",
        verbose_name=_("User"),
    )
    organization = models.ForeignKey(
        Organization,
        on_delete=models.CASCADE,
        related_name="requests",
        verbose_name=_("Organization"),
    )

    def accept_request(self) -> bool:
        """Accept the organization request and create a profile."""
        if not self.user.has_perm(Organization.PERM_MANAGE_REQUESTS, self.organization):
            logger.warning("Attempted to accept organization request by unauthorized user.")
            return False

        # TODO: user notification system

        if not OrganizationProfile.does_profile_exist(user=self.user, organization=self.organization):
            OrganizationProfile.objects.create(user=self.user, organization=self.organization)
            logger.info(
                "Accepted organization request for %s to %s",
                self.user.name,
                self.organization.slug,
            )
            self.delete()
            return True

        logger.warning(
            "Profile already exists for %s in %s",
            self.user.name,
            self.organization.slug,
        )
        self.delete()
        return False

    def reject_request(self) -> bool:
        """Reject the organization request."""
        if not self.user.has_perm(Organization.PERM_MANAGE_REQUESTS, self.organization):
            logger.warning("Attempted to reject organization request by unauthorized user.")
            return False

        # TODO: user notification system

        logger.info("Rejected organization request for %s to %s", self.user.name, self.organization.slug)
        self.delete()
        return True

    def __str__(self):
        return self.user.name + " applying to " + self.organization.slug
