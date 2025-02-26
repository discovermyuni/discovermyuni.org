from .exceptions import InvalidFilterParameterError
from .models import Post


def get_filter_parameters(request):
    page = request.GET.get("page", 10)
    tags = request.GET.getlist("t")

    try:
        page = int(page)
    except ValueError as e:
        error_msg = "Invalid page parameter"
        raise InvalidFilterParameterError(error_msg, 400) from e

    return {"page": page, "tags": tags}


def filter_posts(page, tags=None):
    queryset = Post.objects.order_by("-created_at")[:20]
    if tags:
        queryset = queryset.filter(tags__name__in=tags).distinct()

    return queryset
