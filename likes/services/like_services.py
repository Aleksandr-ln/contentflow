from typing import TypedDict

from django.contrib.auth.base_user import AbstractBaseUser
from django.db import IntegrityError, transaction
from django.db.models import Count

from likes.models import Like
from posts.models import Post


class ToggleResult(TypedDict):
    """
    Return type for toggle_like service.
    """
    liked: bool
    likes_count: int


def toggle_like(user: AbstractBaseUser, post: Post) -> ToggleResult:
    """
    Toggle a like for the given (user, post)
    pair in an idempotent and race-safe way.

    Implementation details:
    - DB-level UniqueConstraint(user, post)
    guarantees no duplicates under concurrency.
    - We optimistically try to create a Like;
    on IntegrityError we delete the existing one.
    - We return the current state (liked) and
    the updated likes_count as the source of truth.

    Args:
        user: Authenticated user performing the action.
        post: Post instance to like/unlike.

    Returns:
        ToggleResult: {"liked": bool, "likes_count": int}
    """
    if not user or not getattr(user, "is_authenticated", False):
        raise ValueError("toggle_like requires an authenticated user")

    with transaction.atomic():
        try:
            with transaction.atomic():
                Like.objects.create(user=user, post=post)
            liked = True
        except IntegrityError:
            Like.objects.filter(user=user, post=post).delete()
            liked = False

        likes_count = (
            Like.objects.filter(post=post).aggregate(c=Count("id"))["c"] or 0
        )

    return {"liked": liked, "likes_count": likes_count}
