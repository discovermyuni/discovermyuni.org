from django.conf import settings

from .exceptions import InvalidFilterParameterError
from .models import Post


def raise_value_error():
    raise ValueError

page_parameter = "p"
posts_per_page_parameter = "c"
sort_type_parameter = "s"
author_ids_parameter = "a"
tags_parameter = "t"

posts_per_page_default = int(settings.POSTS_PER_PAGE_DEFAULT) if hasattr(settings, "POSTS_PER_PAGE_DEFAULT") else 15
post_per_page_options = (
    settings.POSTS_PER_PAGE_OPTIONS
    if hasattr(settings, "POSTS_PER_PAGE_DEFAULT")
    else [posts_per_page_default]
)

sort_type_default = settings.POSTS_SORT_TYPE_DEFAULT if hasattr(settings, "POSTS_SORT_TYPE_DEFAULT") else "newest"
sort_type_options = (
    settings.POSTS_SORT_TYPE_OPTIONS if hasattr(settings, "POSTS_SORT_TYPE_OPTIONS") else [sort_type_default]
)

def get_filter_parameters(request):
    try:
        page = int(request.GET.get(page_parameter, 1))
        if page < 1:
            raise_value_error()
    except ValueError as e:
        error_msg = f"Invalid page parameter ({page_parameter}). Must be a positive integer."
        raise InvalidFilterParameterError(error_msg, 400) from e

    try:
        posts_per_page = int(request.GET.get(posts_per_page_parameter, posts_per_page_default))
        if posts_per_page not in post_per_page_options:
            raise_value_error()
    except ValueError as e:
        error_msg = (
            f"Invalid posts per page ({posts_per_page_parameter}). Must be one of {post_per_page_options}."
        )
        raise InvalidFilterParameterError(error_msg, 400) from e

    try:
        sort_type = request.GET.get(sort_type_parameter, sort_type_default)
        if sort_type not in settings.POSTS_SORT_TYPE_OPTIONS:
            raise_value_error()
    except ValueError as e:
        error_msg = (
            f"Invalid sort type ({sort_type_parameter}). Must be one of {sort_type_options}."
        )
        raise InvalidFilterParameterError(error_msg, 400) from e

    author_ids = request.GET.getlist(author_ids_parameter, [])
    tags = request.GET.getlist(tags_parameter, [])

    return {"sort_type": sort_type, "page": page, "author_ids": author_ids, "tags": tags}


def _get_sorted_queryset(sort_type):
    if sort_type == "most_popular":
        return Post.objects.order_by("title")
    if sort_type == "start_date":
        return Post.objects.order_by("start_date")
    if sort_type == "oldest":
        return Post.objects.order_by("created_at")

    return Post.objects.order_by("-created_at")


def _separate_tags(tags):
    include_tags = []
    exclude_tags = []

    for t in tags:
        if t.startswith("!"):
            exclude_tags.append(t[1:])
        else:
            include_tags.append(t)

    return include_tags, exclude_tags


def _create_filters(author_ids, tags):
    filters = {}
    if author_ids:
        filters["author__id__in"] = author_ids

    if tags:
        include_tags, exclude_tags = _separate_tags(tags)
        if len(include_tags) > 0:
            filters["tags__name__in"] = include_tags
        if len(exclude_tags) > 0:
            filters["tags__name__nin"] = exclude_tags

    return filters



def filter_posts(sort_type, page, author_ids=None, tags=None):
    queryset = _get_sorted_queryset(sort_type)
    filters = _create_filters(author_ids, tags)

    if len(filters) > 0:
        queryset = queryset.filter(**filters).distinct()

    return queryset
