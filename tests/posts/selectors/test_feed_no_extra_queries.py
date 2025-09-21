from django.test import TestCase
from django.test.utils import CaptureQueriesContext
from django.db import connection
from django.contrib.auth import get_user_model

from posts.models import Post, Image, Tag
from likes.models import Like
from posts.services.selectors import get_post_feed_for_user

User = get_user_model()


class FeedNoExtraQueriesTests(TestCase):
    def setUp(self) -> None:
        self.author = User.objects.create_user("author", "a@example.com", "x")
        self.viewer = User.objects.create_user("viewer", "v@example.com", "x")
        tags = [Tag.objects.create(name=f"tag{i}") for i in range(2)]
        posts = []
        for i in range(5):
            p = Post.objects.create(author=self.author, caption=f"p{i}")
            Image.objects.create(post=p, image="posts/test.jpg")
            p.tags.add(tags[i % 2])
            Like.objects.create(user=self.author, post=p)
            posts.append(p)

    def test_no_extra_queries_on_attribute_access(self) -> None:
        posts = list(get_post_feed_for_user(self.viewer)[:5])

        with CaptureQueriesContext(connection) as ctx:
            for p in posts:
                _ = p.author.username
                _ = list(p.images.all())
                _ = list(p.tags.all())
                _ = p.likes_count
                _ = p.has_liked
        self.assertLessEqual(len(ctx), 1)
