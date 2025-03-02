from common.decorators import login_required_message
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from posts.forms import PostForm

LOGIN_REQUIRED_MESSAGE = "You need to be logged in to view the dashboard."


@login_required_message(LOGIN_REQUIRED_MESSAGE)
def dashboard_page_view(request):
    return render(request, "dashboard/home.html", {})


@login_required_message(LOGIN_REQUIRED_MESSAGE)
def post_form_view(request):
    if request.method == "POST":
        form = PostForm(request.POST)
        form.instance.author = request.user

        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse("posts:home"))

    else:
        form = PostForm()

    return render(request, "dashboard/post_form.html", {"form": form})
