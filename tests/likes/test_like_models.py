from django.contrib.auth import get_user_model
from django.db.utils import IntegrityError
from django.test import TestCase

from likes.models import Like
from posts.models import Post

User = get_user_model()


class LikeModelTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='likeuser',
            email='likeuser@example.com',
            password='testpass123'
        )
        self.post = Post.objects.create(
            author=self.user,
            caption="Test Post"
        )

    def test_like_str(self):
        like = Like.objects.create(user=self.user, post=self.post)
        expected = f"{self.user.email} likes Post {self.post.id}"
        self.assertEqual(str(like), expected)

    def test_like_unique_together(self):
        Like.objects.create(user=self.user, post=self.post)
        with self.assertRaises(IntegrityError):
            Like.objects.create(user=self.user, post=self.post)

    def test_like_deleted_with_post(self):
        like = Like.objects.create(user=self.user, post=self.post)
        self.post.delete()
        self.assertFalse(Like.objects.filter(id=like.id).exists())

    def test_like_deleted_with_user(self):
        like = Like.objects.create(user=self.user, post=self.post)
        self.user.delete()
        self.assertFalse(Like.objects.filter(id=like.id).exists())
