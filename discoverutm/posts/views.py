from django.shortcuts import render
from django.views.generic import DetailView
from rest_framework import status as http_status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from .exceptions import InvalidFilterParameterError
from .filter import filter_posts
from .filter import get_filter_parameters
from .models import Post
from .serializers import PostSerializer


def home_page_view(request):
    try:
        params = get_filter_parameters(request)
    except InvalidFilterParameterError as e:
        return Response(e.message, status=e.status)

    posts = filter_posts(**params)
    context = {"posts": posts}

    return render(request, "posts/home.html", context)


class PostDetailView(DetailView):
    model = Post
    template_name = "posts/post_detail.html"
    context_object_name = "post"


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
    serializer = PostSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=http_status.HTTP_201_CREATED)

    return Response(serializer.errors, status=http_status.HTTP_400_BAD_REQUEST)
