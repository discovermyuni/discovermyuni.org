import logging
from pathlib import Path
from uuid import uuid4

from common.models import TimeStampedModel
from django.conf import settings
from django.contrib.auth import get_user_model
from django.db import models
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from organizations.models import Organization
from taggit.managers import TaggableManager

logger = logging.getLogger(__name__)
User = get_user_model()


def path_and_rename(instance, fp):
    upload_to = "debug/posts/" if settings.DEBUG else "posts/"
    ext = fp.split(".")[-1]
    filename = f"{instance.pk}.{ext}" if instance.pk else f"{uuid4().hex}.{ext}"
    return Path(upload_to) / filename


class Post(TimeStampedModel):
    title = models.CharField(_("Title"), max_length=255)
    description = models.TextField(_("Description"))
    organization = models.ForeignKey(Organization, verbose_name=_("Organization"), on_delete=models.CASCADE)
    author = models.ForeignKey(User, verbose_name=_("Author"), on_delete=models.CASCADE, null=True, blank=True)
    start_date = models.DateTimeField(_("Start Date"))
    end_date = models.DateTimeField(_("End Date"), null=True, blank=True)
    location = models.CharField(_("Location"), max_length=255)
    tags = TaggableManager(verbose_name=_("Tags"))
    image = models.ImageField(_("Image"), upload_to=path_and_rename, blank=True)
    generation_source = models.CharField(
        _("Generation Source"),
        blank=True,
        default="",
        auto_created=True,
        max_length=255,
    )

    DESCRIPTION_PREVIEW_LENGTH = 25

    def __str__(self):
        return (
            self.title
            + " | "
            + self.description[: self.DESCRIPTION_PREVIEW_LENGTH]
            + ("" if len(self.description) < self.DESCRIPTION_PREVIEW_LENGTH else "...")
        )

    @property
    def is_generated(self):
        return self.generation_source not in (None, "")

    def delete(self, using=None, *, keep_parents=False):
        if self.image:
            try:
                self.image.delete()
            except Exception as e:
                logger.exception("Error deleting image", extra={"error": str(e)})

        super().delete(using=using, keep_parents=keep_parents)

    def get_absolute_url(self):
        return reverse("post-detail", kwargs={"pk": self.pk})

    def get_edit_url(self):
        return reverse("dashboard:edit-post", kwargs={"pk": self.pk})

    def get_delete_url(self):
        return ""
