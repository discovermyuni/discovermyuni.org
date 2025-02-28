from django.conf import settings
from django.core.paginator import Paginator
from django.db.models import Q

from .exceptions import InvalidFilterParameterError
from .models import Post


def raise_value_error():
    raise ValueError


page_parameter = "p"
posts_per_page_parameter = "c"
sort_type_parameter = "s"
author_ids_parameter = "a"
tags_parameter = "t"

posts_per_page_default = int(settings.POSTS_PER_PAGE_DEFAULT)
post_per_page_options = settings.POSTS_PER_PAGE_OPTIONS

sort_type_default = settings.POSTS_SORT_TYPE_DEFAULT
sort_type_options = list(settings.POSTS_SORT_TYPE_ITEMS.keys())


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
        error_msg = f"Invalid posts per page ({posts_per_page_parameter}). Must be one of {post_per_page_options}."
        raise InvalidFilterParameterError(error_msg, 400) from e

    try:
        sort_type = request.GET.get(sort_type_parameter, sort_type_default)
        if sort_type not in sort_type_options:
            raise_value_error()
    except ValueError as e:
        error_msg = f"Invalid sort type ({sort_type_parameter}). Must be one of {sort_type_options}."
        raise InvalidFilterParameterError(error_msg, 400) from e

    author_ids = request.GET.getlist(author_ids_parameter, [])
    tags = request.GET.getlist(tags_parameter, [])

    return {
        "sort_type": sort_type,
        "page": page,
        "posts_per_page": posts_per_page,
        "author_ids": author_ids,
        "tags": tags,
    }


def _get_sorted_queryset(sort_type):
    return Post.objects.order_by(settings.POSTS_SORT_TYPE_ITEMS[sort_type])


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
    exclude_conditions = []

    if author_ids:
        filters["author__id__in"] = author_ids

    if tags:
        include_tags, exclude_tags = _separate_tags(tags)
        if len(include_tags) > 0:
            filters["tags__name__in"] = include_tags
        if len(exclude_tags) > 0:
            exclude_conditions.append(~Q(tags__name__in=exclude_tags))

    return filters, exclude_conditions


def filter_posts(sort_type, page, posts_per_page, author_ids=None, tags=None):
    queryset = _get_sorted_queryset(sort_type)
    filters, exclude_conditions = _create_filters(author_ids, tags)

    if len(filters) > 0 or len(exclude_conditions) > 0:
        queryset = queryset.filter(*exclude_conditions, **filters).distinct()

    paginator = Paginator(queryset, posts_per_page)
    return paginator.get_page(page).object_list
