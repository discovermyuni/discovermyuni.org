from django import forms

from .models import Post


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ["title", "description", "start_date", "end_date", "location", "tags", "image_url"]
