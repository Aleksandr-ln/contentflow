from django.test import TestCase
from django.contrib.auth import get_user_model

from posts.models import Post, Image, Tag
from likes.models import Like
from posts.services.selectors import get_post_feed_for_user

User = get_user_model()


class FeedCorrectnessTests(TestCase):
    def setUp(self) -> None:
        self.author = User.objects.create_user("author", "a@example.com", "x")
        self.viewer = User.objects.create_user("viewer", "v@example.com", "x")

        self.t_python = Tag.objects.create(name="python")
        self.t_django = Tag.objects.create(name="django")

        self.p0 = Post.objects.create(author=self.author, caption="p0")
        self.p1 = Post.objects.create(author=self.author, caption="p1")
        self.p2 = Post.objects.create(author=self.author, caption="p2")

        for p in (self.p0, self.p1, self.p2):
            Image.objects.create(post=p, image="posts/test.jpg")
        self.p0.tags.add(self.t_python)
        self.p1.tags.add(self.t_python, self.t_django)
        self.p2.tags.add(self.t_django)

        Like.objects.create(user=self.author, post=self.p0)
        Like.objects.create(user=self.viewer, post=self.p1)
        Like.objects.create(user=self.author, post=self.p1)

    def test_likes_annotations_and_ordering(self) -> None:
        qs = list(get_post_feed_for_user(self.viewer)[:10])

        self.assertEqual([p.caption for p in qs], ["p2", "p1", "p0"])

        def real_count(post: Post) -> int:
            return Like.objects.filter(post=post).count()

        for p in qs:
            self.assertEqual(p.likes_count, real_count(p))

        mapping = {p.caption: p.has_liked for p in qs}
        self.assertEqual(mapping["p2"], False)
        self.assertEqual(mapping["p1"], True)
        self.assertEqual(mapping["p0"], False)
