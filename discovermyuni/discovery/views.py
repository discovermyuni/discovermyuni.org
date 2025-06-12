from django.shortcuts import render
from organizations.models import Organization
from posts.exceptions import InvalidFilterParameterError
from posts.filter import filter_posts
from posts.filter import get_filter_parameters


def discovery_home(request):
    """
    Renders the discovery home page.
    """
    organizations = Organization.objects.all()
    context = {
        "organizations": organizations,
    }
    return render(request, "discovery/home.html", context)


def organization_posts(request, slug=None):
    try:
        org = Organization.objects.get(slug=slug)
    except Organization.DoesNotExist:
        return render(request, "discovery/404.html", status=404)

    try:
        params = get_filter_parameters(request)
        posts = filter_posts(organization_id=org.id, **params)
        context = {"posts": posts, "params": params}
    except InvalidFilterParameterError:
        context = {"posts": [], "params": {}}

    context["organization"] = org

    return render(request, "discovery/organization_posts.html", context)
