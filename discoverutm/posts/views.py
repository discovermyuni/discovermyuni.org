from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect
from django.http import JsonResponse
from django.shortcuts import render
from django.urls import reverse
from django.urls import reverse_lazy
from django.views.generic import DetailView
from django.views.generic.edit import CreateView
from django.views.generic.edit import DeleteView
from django.views.generic.edit import UpdateView
from rest_framework.decorators import api_view
from rest_framework.response import Response

from .exceptions import InvalidFilterParameterError
from .filter import filter_posts
from .filter import get_filter_parameters
from .forms import PostForm
from .models import Post
from .serializers import PostSerializer


class JsonableResponseMixin:
    """
    Mixin to add JSON support to a form.
    Must be used with an object-based FormView (e.g. CreateView)
    """

    def form_invalid(self, form):
        response = super().form_invalid(form)
        if self.request.accepts("text/html"):
            return response

        return JsonResponse(form.errors, status=400)

    def form_valid(self, form):
        response = super().form_valid(form)
        if self.request.accepts("text/html"):
            return response

        data = {
            "pk": self.object.pk,
        }
        return JsonResponse(data)

class PostCreateView(LoginRequiredMixin, JsonableResponseMixin, CreateView):
    model = Post
    fields = ["name"]

    def dispatch(self, request, *args, **kwargs):
        post = self.get_object()
        if post.author != request.user:
            return JsonResponse({"error": "You are not the author of this post."}, status=403)
        return super().dispatch(request, *args, **kwargs)

class PostUpdateView(LoginRequiredMixin, UpdateView):
    model = Post
    fields = ["title", "description", "start_date", "end_date", "location"]

    def dispatch(self, request, *args, **kwargs):
        post = self.get_object()
        if post.author != request.user:
            return JsonResponse({"error": "You are not the author of this post."}, status=403)
        return super().dispatch(request, *args, **kwargs)

class PostDeleteView(LoginRequiredMixin, DeleteView):
    model = Post
    success_url = reverse_lazy("posts:home")

class PostDetailView(DetailView):
    model = Post
    template_name = "posts/post_detail.html"
    context_object_name = "post"

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

    return render(request, "posts/post_form.html", {"form": form})

def home_page_view(request):
    try:
        params = get_filter_parameters(request)
    except InvalidFilterParameterError as e:
        return Response(e.message, status=e.status)

    posts = filter_posts(**params)
    context = {"posts": posts}

    return render(request, "posts/home.html", context)


@api_view(["GET"])
def get_posts(request):
    try:
        params = get_filter_parameters(request)
    except InvalidFilterParameterError as e:
        return Response(e.message, status=e.status)

    posts = filter_posts(**params)
    serializer = PostSerializer(posts, many=True, context={"request": request})

    return Response(serializer.data)


@api_view(["POST"])
def create_post(request):
    form = PostForm(request.POST)

    if form.is_valid():
        post = PostSerializer(data=form.cleaned_data)
        if post.is_valid():
            post.save()
            return HttpResponseRedirect(reverse("home"))
    return None
    #     return HttpResponseRedirect(reverse("home"))  # noqa: ERA001

    # return HttpResponseRedirect(reverse("home"))  # noqa: ERA001
