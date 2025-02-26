from django import forms

from .models import PostTemplate


class PostTemplateForm(forms.ModelForm):
    class Meta:
        model = PostTemplate
        fields = ["title", "description", "location", "tags", "image_url"]
