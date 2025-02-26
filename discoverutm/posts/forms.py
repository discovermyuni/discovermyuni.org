from common.forms import DateTimeLocalField
from django import forms

from .models import Post


class PostForm(forms.ModelForm):
    start_date = DateTimeLocalField(required=True)
    end_date = DateTimeLocalField(required=True)

    class Meta:
        model = Post
        fields = ["title", "description", "start_date", "end_date", "location", "tags", "image_url"]
