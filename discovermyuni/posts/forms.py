from common.forms import DateTimeLocalField
from django import forms
from taggit.forms import TagWidget

from .models import Post

MAX_IMAGE_SIZE = 10 * 1024 * 1024  # 10MB


class PostForm(forms.ModelForm):
    start_date = DateTimeLocalField(required=True)
    end_date = DateTimeLocalField(required=False)
    image = forms.ImageField(required=False)

    class Meta:
        model = Post
        fields = ["title", "description", "start_date", "end_date", "location", "tags", "image"]
        widgets = {
            "tags": TagWidget(),
        }

    def clean_image(self):
        image = self.cleaned_data.get("image")
        if image:
            # TODO: Scale down image if larger
            if image.size > MAX_IMAGE_SIZE:
                msg = "Image size must be under 10MB."
                raise forms.ValidationError(msg)
        return image
