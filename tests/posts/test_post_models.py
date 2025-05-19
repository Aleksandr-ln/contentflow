from django.contrib.auth import get_user_model
from django.test import TestCase

from posts.models import Image, Post, Tag

User = get_user_model()


class PostModelTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            email='testuser@example.com',
            password='testpass'
        )

    def test_post_str(self):
        post = Post.objects.create(author=self.user, caption="Test caption")
        expected = f"Post by {self.user.email} at {post.created_at}"
        self.assertEqual(str(post), expected)

    def test_tag_str(self):
        tag = Tag.objects.create(name="testtag")
        self.assertEqual(str(tag), "testtag")

    def test_image_str(self):
        post = Post.objects.create(author=self.user, caption="Test caption")
        image = Image.objects.create(post=post, image='test_image.jpg')
        self.assertEqual(str(image), f"Image for post {post.id}")

    def test_post_get_absolute_url(self):
        post = Post.objects.create(author=self.user, caption="Test caption")
        expected_url = f"/users/{self.user.username}/"
        self.assertEqual(post.get_absolute_url(), expected_url)

    def test_image_deleted_with_post(self):
        post = Post.objects.create(author=self.user, caption="Test caption")
        image = Image.objects.create(post=post, image='test.jpg')
        post.delete()
        self.assertFalse(Image.objects.filter(id=image.id).exists())

    def test_post_deleted_with_user(self):
        post = Post.objects.create(author=self.user, caption="Test caption")
        self.user.delete()
        self.assertFalse(Post.objects.filter(id=post.id).exists())
