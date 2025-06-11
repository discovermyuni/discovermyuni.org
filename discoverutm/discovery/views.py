from common.models import Organization
from common.models.organization import OrganizationRequest
from django.http import JsonResponse
from django.shortcuts import render
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


def apply_to_organization(request, organization_id):
    """
    Handles the application to an organization for the authenticated user.
    """
    request_exists = OrganizationRequest.objects.filter(
        user=request.user,
        organization_id=organization_id,
    ).exists()

    if request_exists:
        return JsonResponse(
            {"error": "You have already applied to this organization."},
            status=400,
        )

    OrganizationRequest.objects.create(
        user=request.user,
        organization_id=organization_id,
    )
    return JsonResponse(
        {"message": "Application submitted successfully."},
        status=200,
    )
