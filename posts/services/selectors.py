from django.contrib.auth import get_user_model
from django.db.models import Count, Exists, OuterRef, QuerySet

from likes.models import Like
from posts.models import Post

User = get_user_model()


def get_post_feed_for_user(user: User) -> QuerySet:
    """
    Return queryset of posts for main feed with annotated like info.
    """
    return Post.objects.annotate(
        likes_count=Count('likes', distinct=True),
        has_liked=Exists(
            Like.objects.filter(user=user, post=OuterRef('pk'))
        )
    ).prefetch_related('images', 'tags', 'author').order_by('-created_at')


def get_posts_by_tag_for_user(user: User, tag_name: str) -> QuerySet:
    """
    Return queryset of posts filtered by tag with like annotations.
    """
    return Post.objects.filter(tags__name=tag_name.lower()).annotate(
        likes_count=Count('likes', distinct=True),
        has_liked=Exists(
            Like.objects.filter(user=user, post=OuterRef('pk'))
        )
    ).prefetch_related('images', 'tags', 'author').order_by('-created_at')


def get_posts_by_user(viewed_user: User, viewer: User) -> QuerySet:
    """
    Return a queryset of posts authored by viewed_user,
    annotated with like info for the current viewer.
    """
    return Post.objects.filter(author=viewed_user).annotate(
        likes_count=Count('likes', distinct=True),
        has_liked=Exists(
            Like.objects.filter(user=viewer, post=OuterRef('pk'))
        )
    ).prefetch_related('images', 'tags').order_by('-created_at')
