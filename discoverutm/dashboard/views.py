from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from posts.forms import PostForm


@login_required
def dashboard_page_view(request):
    return render(request, "dashboard/home.html", {})


@login_required
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
