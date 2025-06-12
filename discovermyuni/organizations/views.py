from common.decorators import login_required_message
from django.contrib.auth import get_user_model
from django.rest_framework.decorators import api_view
from django.rest_framework.decorators import permission_classes
from django.rest_framework.permissions import IsAuthenticated
from django.rest_framework.response import Response
from django.shortcuts import render

from .models import OrganizationRequest

User = get_user_model()


@login_required_message()
def manage_organizations(request):
    """
    Returns a list of organizations the authenticated user is part of.
    """
    return render(request, "organizations/manage_organizations.html")


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def user_organizations(request):
    """
    Returns a list of organizations the authenticated user is part of.
    """


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def apply_to_organization(request, organization_id):
    """
    Handles the application to an organization for the authenticated user.
    """
    request_exists = OrganizationRequest.objects.filter(
        user=request.user,
        organization_id=organization_id,
    ).exists()

    if request_exists:
        return Response(
            {"error": "You have already applied to this organization."},
            status=400,
        )

    OrganizationRequest.objects.create(
        user=request.user,
        organization_id=organization_id,
    )
    return Response(
        {"message": "Application submitted successfully."},
        status=200,
    )
