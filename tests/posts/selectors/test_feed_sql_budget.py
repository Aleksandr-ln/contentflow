from django.test import TestCase
from django.test.utils import CaptureQueriesContext
from django.db import connection
from django.contrib.auth import get_user_model

from posts.models import Post, Image, Tag
from likes.models import Like
from posts.services.selectors import get_post_feed_for_user

User = get_user_model()


class FeedSQLBudgetTests(TestCase):
    def setUp(self) -> None:
        self.author = User.objects.create_user(
            username="author",
            email="author@example.com",
            password="pass",
        )
        self.viewer = User.objects.create_user(
            username="viewer",
            email="viewer@example.com",
            password="pass",
        )

        tags = [Tag.objects.create(name=f"tag{i}") for i in range(3)]

        for i in range(10):
            p = Post.objects.create(author=self.author, caption=f"post {i}")
            Image.objects.create(post=p, image="posts/test.jpg")
            Image.objects.create(post=p, image="posts/test2.jpg")
            p.tags.add(tags[i % 3], tags[(i + 1) % 3])
            Like.objects.create(user=self.author, post=p)

    def test_feed_sql_budget(self) -> None:
        """
        The feed selector must not trigger N+1 queries.
        Budget: <= 6 queries for 10 posts with images and tags.
        """
        with CaptureQueriesContext(connection) as ctx:
            posts = list(get_post_feed_for_user(self.viewer)[:10])

        for post in posts:
            _ = post.author.username
            _ = list(post.images.all())
            _ = list(post.tags.all())
            _ = post.likes_count
            _ = post.has_liked

        self.assertLessEqual(len(ctx), 6)
