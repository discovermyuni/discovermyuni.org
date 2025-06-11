from pathlib import Path
from urllib.parse import quote
from uuid import uuid4

from common.models import TimeStampedModel
from django.conf import settings
from django.contrib.auth import get_user_model
from django.db import models
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from posts.models import PostLocation
from taggit.managers import TaggableManager

User = get_user_model()


def path_and_rename(instance, fp):
    upload_to = "debug/post-templates/" if settings.DEBUG else "post-templates/"
    ext = fp.split(".")[-1]
    filename = f"{instance.pk}.{ext}" if instance.pk else f"{uuid4().hex}.{ext}"
    return Path(upload_to) / filename


class PostTemplate(TimeStampedModel):
    title = models.CharField(_("Title"), max_length=255)
    description = models.TextField(_("Description"))
    author = models.ForeignKey(User, verbose_name=_("Author"), null=True, blank=True, on_delete=models.CASCADE)
    location = models.ForeignKey(PostLocation, verbose_name=_("Location"), on_delete=models.PROTECT, null=True)
    tags = TaggableManager(verbose_name=_("Tags"))
    image = models.ImageField(_("Image"), upload_to=path_and_rename, blank=True)

    DESCRIPTION_PREVIEW_LENGTH = 25

    def __str__(self):
        return (
            self.title + " | " + self.description[: self.DESCRIPTION_PREVIEW_LENGTH] + ""
            if len(self.description) < self.DESCRIPTION_PREVIEW_LENGTH
            else "..."
        )

    def get_form_url(self):
        kwargs = {
            "title": self.title,
            "description": self.description,
            "location_id": self.location.name if self.location else None,
            "tags": ",".join(tag.name for tag in self.tags.all()),
            "image": self.image.url if self.image else None,
        }
        # URL-encode the parameters
        kwargs = {k: quote(str(v)) for k, v in kwargs.items() if v is not None}
        query_string = "&".join(f"{k}={v}" for k, v in kwargs.items())
        return f"{reverse('dashboard:new-post')}?{query_string}"
