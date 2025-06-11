from common.forms import DateTimeLocalField
from django import forms

from .models import Post

MAX_IMAGE_SIZE = 10 * 1024 * 1024  # 10MB


class PostForm(forms.ModelForm):
    start_date = DateTimeLocalField(required=True)
    end_date = DateTimeLocalField(required=False)
    image = forms.ImageField(required=False)
    tags = forms.CharField(
        max_length=255,
        label="Tags",
        required=False,
        initial="",
        help_text="Comma-separated list of tags. E.g. tag1, tag2, tag3",
    )

    class Meta:
        model = Post
        fields = ["title", "description", "start_date", "end_date", "location", "tags", "image"]

    def save(self, commit=True):  # noqa: FBT002
        instance = super().save(commit=False)
        tag_string = self.cleaned_data.get("tags", "")
        tag_list = [tag.strip() for tag in tag_string.split(",") if tag.strip()]
        if commit:
            instance.save()
            instance.tags.set(*tag_list)
        else:
            self._pending_tags = tag_list  # store tags for later
        return instance

    def save_m2m(self):
        super().save_m2m()
        if hasattr(self, "_pending_tags"):
            self.instance.tags.set(*self._pending_tags)

    def clean_image(self):
        image = self.cleaned_data.get("image")
        if image:
            # TODO: Scale down image if larger
            if image.size > MAX_IMAGE_SIZE:
                msg = "Image size must be under 10MB."
                raise forms.ValidationError(msg)
        return image
