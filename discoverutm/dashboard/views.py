from urllib.parse import unquote

from common.decorators import login_required_message
from django.conf import settings
from django.contrib import messages
from django.contrib.auth import get_user_model
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from posts.forms import PostForm

from .forms import PostTemplateForm

User = get_user_model()
LOGIN_REQUIRED_MESSAGE = _("You need to be logged in to view the dashboard.")

VALID_POST_FORM_FIELDS = (
    settings.VALID_POST_FORM_FIELDS
    if hasattr(settings, "VALID_POST_FORM_FIELDS")
    else ["title", "description", "location", "tags", "image"]
)

# TODO: localize all this


@login_required_message(LOGIN_REQUIRED_MESSAGE)
def dashboard_page_view(request):
    user_posts = request.user.post_set.all()
    user_post_templates = request.user.posttemplate_set.all()
    context = {
        "user_posts": user_posts,
        "user_post_templates": user_post_templates,
    }
    return render(request, "dashboard/home.html", context)


@login_required_message(LOGIN_REQUIRED_MESSAGE)
def post_form_view(request):
    if request.method == "POST":
        form = PostForm(request.POST)
        form.instance.author = request.user

        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse("dashboard:home"))

    else:
        initial_data = request.GET.dict()
        sanitized_data = {}

        for k, v in initial_data.items():
            if k in VALID_POST_FORM_FIELDS and v is not None:
                sanitized_data[k] = unquote(v)

        form = PostForm(initial=sanitized_data)

    return render(request, "dashboard/forms/new_post.html", {"form": form})


@login_required_message(LOGIN_REQUIRED_MESSAGE)
def post_template_form_view(request):
    if request.method == "POST":
        form = PostTemplateForm(request.POST)
        form.instance.author = request.user

        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse("dashboard:home"))

    else:
        form = PostForm()

    return render(request, "dashboard/forms/new_post_template.html", {"form": form})


@login_required_message(LOGIN_REQUIRED_MESSAGE)
def post_edit_view(request, pk):
    try:
        post = request.user.post_set.get(pk=pk)
    except request.user.post_set.model.DoesNotExist:
        messages.error(request, "Post " + str(pk) + " not found.")
        return HttpResponseRedirect(reverse("dashboard:home"))

    if post.author != request.user:
        messages.error(request, "Post " + str(pk) + " does not exist or you are not the owner.")
        return HttpResponseRedirect(reverse("dashboard:home"))

    if request.method == "POST":
        form = PostForm(request.POST, instance=post)
        form.instance.author = request.user

        if form.is_valid():
            form.save()
            messages.success(request, "Post updated successfully.")
        else:
            messages.error(request, "There was an error updating your post. Reason: " + str(form.errors))
        return HttpResponseRedirect(reverse("dashboard:home"))

    form = PostForm(instance=post)
    return render(request, "dashboard/forms/edit_post.html", {"form": form})
