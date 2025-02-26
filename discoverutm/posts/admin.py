from django.contrib import admin

from .models import Post
from .models import PostLocation

admin.site.register(Post)
admin.site.register(PostLocation)
