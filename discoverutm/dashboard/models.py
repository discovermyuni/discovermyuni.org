from common.models import TimeStampedModel
from django.contrib.auth import get_user_model
from django.db import models
from django.utils.translation import gettext_lazy as _
from posts.models import PostLocation
from taggit.managers import TaggableManager

User = get_user_model()


class PostTemplate(TimeStampedModel):
    title = models.CharField(_("Title"), max_length=255)
    description = models.TextField(_("Description"))
    author = models.ForeignKey(User, verbose_name=_("Author"), null=True, blank=True, on_delete=models.CASCADE)
    location = models.ForeignKey(PostLocation, verbose_name=_("Location"), on_delete=models.PROTECT, null=True)
    tags = TaggableManager(verbose_name=_("Tags"))
    is_public = models.BooleanField(_("Is Public?"), default=False)

    DESCRIPTION_PREVIEW_LENGTH = 25

    def __str__(self):
        return (
            self.title + " | " + self.description[: self.DESCRIPTION_PREVIEW_LENGTH] + ""
            if len(self.description) < self.DESCRIPTION_PREVIEW_LENGTH
            else "..."
        )

    def convert_to_post(self, start_date, end_date, new_title=None, new_description=None, new_location=None):
        # raise error if location is null and new location is None
        # same w title and description
        pass
