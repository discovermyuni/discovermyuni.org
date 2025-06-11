from django import forms
from django.contrib import admin
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

from .models import Post
from .models import PostLocation

admin.site.register(PostLocation)


class PostAdminForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = [
            "title",
            "description",
            "organization",
            "start_date",
            "end_date",
            "author",
            "location",
            "tags",
            "image",
        ]

    def clean(self):
        cleaned_data = super().clean()
        org = cleaned_data.get("organization")
        loc = cleaned_data.get("location")

        if loc and org and loc.organization != org:
            raise ValidationError(_("Location must belong to the same organization as the post."))
        return cleaned_data


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    form = PostAdminForm
