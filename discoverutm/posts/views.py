from django.views.generic import DetailView
from django.views.generic import TemplateView
from rest_framework import status as http_status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from .filter import filter_posts
from .models import Post
from .serializers import PostSerializer


def get_filter_parameters(request):
    page = request.GET.get("page", 10)
    tags = request.GET.getlist("t")

    try:
        page = int(page)
    except ValueError:
        return http_status.HTTP_400_BAD_REQUEST, {"error": "Invalid value for parameter page"}

    return http_status.HTTP_200_OK, {"page": page, "tags": tags}


class HomePageView(TemplateView):
    template_name = "posts/home.html"

    def get(self, request, *args, **kwargs):
        status, params = get_filter_parameters(request)
        if status != http_status.HTTP_200_OK:
            return Response(params["error"], status=status)

        self.page = params["page"]
        self.tags = params["tags"]

        return super().get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["posts"] = filter_posts(page=self.page)

        return context


class PostDetailView(DetailView):
    model = Post
    template_name = "posts/post_detail.html"
    context_object_name = "post"


@api_view(["GET"])
def get_posts(request):
    status, params = get_filter_parameters(request)

    if status != http_status.HTTP_200_OK:
        return Response(params["error"], status=status)

    page = params["page"]
    tags = params["tags"]

    queryset = filter_posts(page=page, tags=tags)
    serializer = PostSerializer(queryset, many=True, context={"request": request})

    return Response(serializer.data)
