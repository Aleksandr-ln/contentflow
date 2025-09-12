from django.contrib.auth.decorators import login_required
from django.http import HttpRequest, JsonResponse
from django.shortcuts import get_object_or_404
from django.views.decorators.http import require_POST

from posts.models import Post

from .services.like_services import toggle_like


@require_POST
@login_required
def like_toggle_ajax(request: HttpRequest) -> JsonResponse:
    """
    AJAX endpoint to toggle like for a given post.

    Contract (unchanged for frontend):
    - Accepts POST form data with "post_id".
    - Returns JSON with keys: "liked" (bool),
    "likes_count" (int), "post_id" (int).
    """
    if request.headers.get("x-requested-with") != "XMLHttpRequest":
        return JsonResponse({"error": "Invalid request type"}, status=400)

    post_id_raw = request.POST.get("post_id")
    if not post_id_raw:
        return JsonResponse({"error": "post_id is required"}, status=400)

    try:
        post_id = int(post_id_raw)
    except (TypeError, ValueError):
        return JsonResponse(
            {"error": "post_id must be an integer"},
            status=400
        )

    post: Post = get_object_or_404(Post, id=post_id)

    result = toggle_like(user=request.user, post=post)

    return JsonResponse(
        {
            "liked": result["liked"],
            "likes_count": result["likes_count"],
            "post_id": post.id,
        },
        status=200,
    )
