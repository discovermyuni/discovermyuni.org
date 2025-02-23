from django.contrib.auth import get_user_model
from django.db import models
from taggit.managers import TaggableManager

User = get_user_model()

# TODO: move timestamped model to common app
# TODO: add location model(?) so its dynamically configurable, plus a validation for pre-existing posts

class TimeStampedModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Post(TimeStampedModel):
    title = models.CharField(max_length=255)
    description = models.TextField()
    creator = models.ForeignKey(User, on_delete=models.CASCADE)
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    location = models.CharField(max_length=255, choices=[
        ("MN2170", "MN2170"),
        ("IB120", "IB120"),
        ("DV2074", "DV2074"),
    ])
    tags = TaggableManager()


    DESCRIPTION_PREVIEW_LENGTH = 25

    def __str__(self):
        return self.title + " | " + self.description[:self.DESCRIPTION_PREVIEW_LENGTH] + \
               "" if len(self.description) < self.DESCRIPTION_PREVIEW_LENGTH else "..."
