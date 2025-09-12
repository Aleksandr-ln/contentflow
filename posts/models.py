from typing import Any

from django.conf import settings
from django.db import models
from django.db.models import UniqueConstraint
from django.db.models.functions import Lower
from django.urls import reverse


class Tag(models.Model):
    """Normalized, case-insensitive unique tag."""
    name = models.CharField(max_length=30, unique=True)

    class Meta:
        constraints = [
            UniqueConstraint(
                Lower("name"),
                name="uniq_tag_name_lower",
            ),
        ]

    def save(self, *args: Any, **kwargs: Any) -> None:
        """Normalize to lowercase for consistency (defense-in-depth)."""
        if self.name:
            self.name = self.name.strip().lower()
        super().save(*args, **kwargs)

    def __str__(self) -> str:
        return self.name


class Post(models.Model):
    """
    Post model representing user-created content with text, tags, and images.
    """

    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="posts"
    )
    caption = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    tags = models.ManyToManyField(Tag, related_name="posts", blank=True)

    def get_absolute_url(self):
        return reverse('users:profile', args=[self.author.username])

    def __str__(self) -> str:
        return f"Post by {self.author.email} at {self.created_at}"


class Image(models.Model):
    """
    Image model attached to a post, allowing multiple images per post.
    """

    post = models.ForeignKey(
        Post, on_delete=models.CASCADE, related_name="images"
    )
    image = models.ImageField(upload_to="posts/")
    thumbnail = models.ImageField(
        upload_to="posts/thumbnails/", blank=True, null=True
    )

    def __str__(self) -> str:
        return f"Image for post {self.post.id}"
