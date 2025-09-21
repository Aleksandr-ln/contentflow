from typing import Final
from typing import TYPE_CHECKING
from django.db.models import Count, Exists, OuterRef, Prefetch, QuerySet

from likes.models import Like
from posts.models import Post, Image, Tag

if TYPE_CHECKING:
    from users.models import User

IMAGES_QS: Final = (
    Image.objects.only("id", "post_id", "image", "thumbnail").order_by("id")
)
TAGS_QS: Final = Tag.objects.only("id", "name").order_by("name")


def _base_feed_qs(viewer: "User") -> QuerySet[Post]:
    """
    Build the base queryset for posts with anti-N+1 guarantees.

    - `select_related("author")` joins FK to avoid extra queries per post.
    - `prefetch_related` batches images & tags into 2 additional queries.
    - `annotate` computes likes_count and has_liked in the main SELECT.
    - `only(...)` keeps row width minimal (I/O & deserialization savings).
    - Secondary order by "-id" stabilizes ordering for identical timestamps.

    Returns:
        QuerySet[Post]: Lightweight, slice-ready queryset for pagination.
    """
    return (
        Post.objects.select_related("author")
        .prefetch_related(
            Prefetch("images", queryset=IMAGES_QS),
            Prefetch("tags", queryset=TAGS_QS),
        )
        .annotate(
            likes_count=Count("likes", distinct=True),
            has_liked=Exists(
                Like.objects.filter(user=viewer, post=OuterRef("pk"))
            ),
        )
        .only("id", "author_id", "caption", "created_at")
        .order_by("-created_at", "-id")
    )


def get_post_feed_for_user(user: "User") -> QuerySet[Post]:
    """
    Main feed queryset (anti-N+1).

    Returns:
        QuerySet[Post]: Optimized queryset of latest posts for the feed.
    """
    return _base_feed_qs(viewer=user)


def get_posts_by_tag_for_user(user: "User", tag_name: str) -> QuerySet[Post]:
    """
    Tag-filtered feed (anti-N+1).

    Args:
        user: Current viewer (used for has_liked).
        tag_name: Tag name to filter by (case-insensitive).

    Returns:
        QuerySet[Post]: Optimized queryset filtered by tag.
    """
    return _base_feed_qs(viewer=user).filter(tags__name=tag_name.lower())


def get_posts_by_user(viewed_user: "User", viewer: "User") -> QuerySet[Post]:
    """
    Profile feed (posts by a specific author) with anti-N+1.

    Args:
        viewed_user: Author whose posts are listed.
        viewer: Current viewer (used for has_liked).

    Returns:
        QuerySet[Post]: Optimized queryset of posts by `viewed_user`.
    """
    return _base_feed_qs(viewer=viewer).filter(author=viewed_user)
