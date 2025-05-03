import logging
from pathlib import Path
from uuid import uuid4

from common.models import TimeStampedModel
from django.conf import settings
from django.contrib.auth import get_user_model
from django.db import models
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from taggit.managers import TaggableManager

logger = logging.getLogger(__name__)
User = get_user_model()


def path_and_rename(instance, fp):
    upload_to = "debug/posts/" if settings.DEBUG else "posts/"
    ext = fp.split(".")[-1]
    filename = f"{instance.pk}.{ext}" if instance.pk else f"{uuid4().hex}.{ext}"
    return Path(upload_to) / filename


class PostLocation(models.Model):
    name = models.CharField(_("Name"), max_length=255, primary_key=True)

    def __str__(self):
        return self.name


class Post(TimeStampedModel):
    title = models.CharField(_("Title"), max_length=255)
    description = models.TextField(_("Description"))
    author = models.ForeignKey(User, verbose_name=_("Author"), on_delete=models.CASCADE)
    start_date = models.DateTimeField(_("Start Date"))
    end_date = models.DateTimeField(_("End Date"))
    location = models.ForeignKey(PostLocation, verbose_name=_("Location"), on_delete=models.PROTECT)
    tags = TaggableManager(verbose_name=_("Tags"))
    image = models.ImageField(_("Image"), upload_to=path_and_rename, blank=True)

    DESCRIPTION_PREVIEW_LENGTH = 25

    def __str__(self):
        return (
            self.title
            + " | "
            + self.description[: self.DESCRIPTION_PREVIEW_LENGTH]
            + ("" if len(self.description) < self.DESCRIPTION_PREVIEW_LENGTH else "...")
        )

    def delete(self, using=None, *, keep_parents=False):
        if self.image:
            try:
                self.image.delete()
            except Exception as e:
                logger.exception("Error deleting image", extra={"error": str(e)})

        super().delete(using=using, keep_parents=keep_parents)

    def get_absolute_url(self):
        return reverse("posts:post-detail", kwargs={"pk": self.pk})
