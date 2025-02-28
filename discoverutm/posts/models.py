from common.models import TimeStampedModel
from django.contrib.auth import get_user_model
from django.db import models
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from taggit.managers import TaggableManager

User = get_user_model()



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
    image = models.ImageField(_("Image"), blank=True)

    DESCRIPTION_PREVIEW_LENGTH = 25

    def __str__(self):
        return self.title + " | " + self.description[:self.DESCRIPTION_PREVIEW_LENGTH] + \
               "" if len(self.description) < self.DESCRIPTION_PREVIEW_LENGTH else "..."

    def get_absolute_url(self):
        return reverse("posts:post-detail", kwargs={"pk": self.pk})
