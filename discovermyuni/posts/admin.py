from django import forms
from django.contrib import admin

from .models import Post


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


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    form = PostAdminForm
