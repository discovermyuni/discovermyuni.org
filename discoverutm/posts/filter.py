from .exceptions import InvalidFilterParameterError
from .models import Post


def raise_value_error():
    raise ValueError


def get_filter_parameters(request):
    try:
        page = int(request.GET.get("page", 1))
        if page < 1:
            raise_value_error()

    except ValueError as e:
        error_msg = "Invalid page parameter. Must be a positive integer."
        raise InvalidFilterParameterError(error_msg, 400) from e

    author_ids = request.GET.getlist("a", [])
    tags = request.GET.getlist("t", [])


    return {"page": page, "author_ids": author_ids, "tags": tags}


def filter_posts(page, author_ids=None, tags=None):
    # TODO: add page restriction
    queryset = Post.objects.order_by("-created_at")

    filters = {}
    if author_ids:
        filters["author__id__in"] = author_ids

    if tags:
        include_tags = []
        exclude_tags = []

        for t in tags:
            if t.startswith("!"):
                exclude_tags.append(t[1:])
            else:
                include_tags.append(t)

        if len(include_tags) > 0:
            filters["tags__name__in"] = include_tags
        if len(exclude_tags) > 0:
            filters["tags__name__nin"] = exclude_tags

    if len(filters) > 0:
        queryset = queryset.filter(**filters).distinct()

    return queryset
