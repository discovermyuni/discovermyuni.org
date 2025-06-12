from django.conf import settings
from django.contrib.auth import get_user_model
from django.shortcuts import render
from django.views.generic import DetailView
from rest_framework.decorators import api_view
from rest_framework.decorators import permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .exceptions import InvalidFilterParameterError
from .filter import filter_posts
from .filter import get_filter_parameters
from .models import Post
from .serializers import PostSerializer

User = get_user_model()


class PostDetailView(DetailView):
    model = Post
    template_name = "posts/detail.html"
    context_object_name = "post"


# api views
@api_view(["GET"])
@permission_classes([IsAuthenticated])
def fetch_posts(request):
    try:
        params = get_filter_parameters(request)
        posts = filter_posts(**params)
    except InvalidFilterParameterError as e:
        return Response({"error": e.error_message}, status=400)

    serializer = PostSerializer(posts, many=True, context={"request": request})
    return Response(serializer.data, status=200)


@api_view(["GET"])
def render_cards(request):
    try:
        params = get_filter_parameters(request)
        posts = filter_posts(**params)
        context = {"posts": posts, "params": params}
    except InvalidFilterParameterError:
        context = {"posts": [], "params": {}}

    return render(request, "posts/render_cards.html", context)


@api_view(["POST"])
def publish_post(request):
    # under the assumption that communication is done safely via HTTPS
    # eventually use a more secure method for bot publishing but for now its full trust in the api key
    # FUTURE REYAAN: ngl this feels sus
    api_key = request.headers.get("x-Api-Key")

    if not api_key:
        return Response({"error": "No API key provided."}, status=403)

    if api_key != settings.BOT_PUBLISH_API_KEY:
        return Response({"error": "Invalid API key."}, status=403)

    # collate all allowed keys and pass them to the serializer
    allowed_fields = {
        field_name for field_name, field_obj in PostSerializer().get_fields().items() if not field_obj.read_only
    }
    cleaned_data = {key: value for key, value in request.data.items() if key in allowed_fields}

    # add image from multipart form data if it exists
    # TODO: make this common between the dashboard and this
    if "image" in allowed_fields and "image" in request.FILES:
        img = request.FILES["image"]

        if img.size > settings.MAX_IMAGE_SIZE:
            return Response({"error": "Image size exceeds the maximum limit."}, status=400)
        if img.size <= 0:
            return Response({"error": "Image size must be greater than 0."}, status=400)

        cleaned_data["image"] = img

    serializer = PostSerializer(data=cleaned_data)

    if serializer.is_valid():
        # bind to anon if author is not provided
        # this is the 'full trust' part of the bot publishing
        author_id = request.data["author_id"].strip().lower()
        try:
            author = User.objects.get(pk=author_id)
        except User.DoesNotExist:
            author = None

        # make it clear where it came from and that its generated for clarity
        generation_source = (
            request.data["generation_source"].strip() if "generation_source" in request.data else "unknown"
        )

        serializer.save(author=author, generation_source=generation_source)
        return Response(status=200)

    return Response(serializer.errors, status=400)
