from urllib.parse import unquote

from common.decorators import login_required_message
from django.conf import settings
from django.contrib.auth import get_user_model
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from posts.forms import PostForm

from .forms import PostTemplateForm

User = get_user_model()
LOGIN_REQUIRED_MESSAGE = "You need to be logged in to view the dashboard."

VALID_POST_FORM_FIELDS = (
    settings.VALID_POST_FORM_FIELDS
    if hasattr(settings, "VALID_POST_FORM_FIELDS")
    else ["title", "description", "location", "tags", "image"]
)


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

    return render(request, "dashboard/post_form.html", {"form": form})


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

    return render(request, "dashboard/post_template_form.html", {"form": form})
