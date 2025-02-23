from .models import Post


def filter_posts(page, tags=None):
    queryset = Post.objects.order_by("-created_at")[:20]
    if tags:
        queryset = queryset.filter(tags__name__in=tags).distinct()

    return queryset
