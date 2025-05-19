from django.contrib.auth.decorators import login_required
from django.http import HttpRequest, JsonResponse
from django.shortcuts import get_object_or_404
from django.views.decorators.http import require_POST

from posts.models import Post

from .models import Like


@require_POST
@login_required
def like_toggle_ajax(request: HttpRequest) -> JsonResponse:
    """
    Toggle like status for a post via AJAX request.

    Accepts POST data with `post_id`.
    If the user has already liked the post, the like is removed.
    Otherwise, a new like is created.

    Returns:
        JsonResponse: A JSON object with:
            - liked (bool): Whether the post is liked after the toggle.
            - likes_count (int): Total number of likes for the post.
            - post_id (int): ID of the affected post.
    """
    if request.headers.get('x-requested-with') != 'XMLHttpRequest':
        return JsonResponse({"error": "Invalid request type"}, status=400)

    post_id: str | None = request.POST.get("post_id")
    if not post_id:
        return JsonResponse({"error": "post_id is required"}, status=400)
    post: Post = get_object_or_404(Post, id=post_id)
    user = request.user

    like_obj, created = Like.objects.get_or_create(user=user, post=post)
    if not created:
        like_obj.delete()
        liked: bool = False
    else:
        liked = True

    likes_count: int = post.likes.count()

    return JsonResponse({
        "liked": liked,
        "likes_count": likes_count,
        "post_id": post.id,
    })
