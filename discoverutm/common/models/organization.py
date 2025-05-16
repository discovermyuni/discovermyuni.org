import logging

from common.models import TimeStampedModel
from django.contrib.auth import get_user_model
from django.db import models
from django.urls import reverse
from django.utils.translation import gettext_lazy as _

logger = logging.getLogger(__name__)
User = get_user_model()


class Organization(TimeStampedModel):
    title = models.CharField(_("Title"), max_length=255)
    slug = models.CharField(_("Slug"), max_length=255, unique=True)
    description = models.TextField(_("Description"))

    def __str__(self):
        return self.title + " | " + self.slug

    def get_absolute_url(self):
        return reverse("discovery:organization_posts", args=[self.slug])
