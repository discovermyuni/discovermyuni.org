from django.views.generic import TemplateView
from rest_framework.decorators import api_view
from rest_framework.response import Response

from .filter import filter_posts
from .serializers import PostSerializer

# TODO: add post view instead of using modal
# TODO: add AJAX to reload posts based on filtering

class HomePageView(TemplateView):
    template_name = "posts/home.html"

    def get(self, request, *args, **kwargs):
        self.page = int(request.GET.get("page", 1))
        return super().get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["posts"] = filter_posts(self.page)
        context["page"] = self.page

        return context



@api_view(["GET"])
def get_posts(request):
    n = request.GET.get("n", 10)
    tags = request.GET.getlist("t")

    try:
        n = int(n)
    except ValueError:
        return Response({"error": "Invalid value for parameter n"}, status=400)

    # TODO: use rest api's pagination? or add custom pagination
    # TODO: sorting filters (needs to be in sort.py?)
    # TODO: mimic over on the homepage/build a common function
    # TODO: add more basic filters

    queryset = filter_posts(page=n, tags=tags)
    serializer = PostSerializer(queryset, many=True)

    return Response(serializer.data)
