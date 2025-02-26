from django.contrib.auth import get_user_model
from django.db import models
from django.utils.translation import gettext_lazy as _
from taggit.managers import TaggableManager

User = get_user_model()

class TimeStampedModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class PostLocation(models.Model):
    name = models.CharField(_("Name"), max_length=255)

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


    DESCRIPTION_PREVIEW_LENGTH = 25

    def __str__(self):
        return self.title + " | " + self.description[:self.DESCRIPTION_PREVIEW_LENGTH] + \
               "" if len(self.description) < self.DESCRIPTION_PREVIEW_LENGTH else "..."


class PostTemplate(TimeStampedModel):
    title = models.CharField(_("Title"), max_length=255)
    description = models.TextField(_("Description"))
    author = models.ForeignKey(User, verbose_name=_("Author"), on_delete=models.CASCADE)
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
