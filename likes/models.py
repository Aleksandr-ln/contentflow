from django.conf import settings
from django.db import models

from django.db.models import UniqueConstraint
from posts.models import Post


class Like(models.Model):
    """
    Unique 'like' from user to post.
    """
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="likes"
    )
    post = models.ForeignKey(
        Post,
        on_delete=models.CASCADE,
        related_name="likes"
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [
            UniqueConstraint(
                fields=["user", "post"],
                name="uniq_like_user_post"
            ),
        ]

    def __str__(self) -> str:
        return f"{self.user.email} likes Post {self.post.id}"
