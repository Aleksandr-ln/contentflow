from django.test import TestCase
from django.contrib.auth import get_user_model

from posts.models import Post, Tag
from posts.services.selectors import get_posts_by_tag_for_user, get_posts_by_user

User = get_user_model()


class FeedFilterTests(TestCase):
    def setUp(self) -> None:
        self.author = User.objects.create_user("author", "a@example.com", "x")
        self.viewer = User.objects.create_user("viewer", "v@example.com", "x")
        self.other = User.objects.create_user("other", "o@example.com", "x")

        self.t_python = Tag.objects.create(name="python")
        self.t_django = Tag.objects.create(name="django")

        self.p_auth_0 = Post.objects.create(author=self.author, caption="a0")
        self.p_auth_1 = Post.objects.create(author=self.author, caption="a1")
        self.p_other_0 = Post.objects.create(author=self.other, caption="o0")

        self.p_auth_0.tags.add(self.t_python)
        self.p_auth_1.tags.add(self.t_django)
        self.p_other_0.tags.add(self.t_python)

    def test_get_posts_by_tag_case_insensitive(self) -> None:
        out = list(get_posts_by_tag_for_user(self.viewer, "PyThOn"))
        caps = sorted(p.caption for p in out)
        self.assertEqual(caps, ["a0", "o0"])

    def test_get_posts_by_user_only_that_author(self) -> None:
        out = list(get_posts_by_user(self.author, self.viewer))
        caps = sorted(p.caption for p in out)
        self.assertEqual(caps, ["a0", "a1"])
