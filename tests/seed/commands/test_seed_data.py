from io import BytesIO
from unittest.mock import patch

from django.contrib.auth import get_user_model
from django.core.management import call_command
from django.test import TestCase

from posts.models import Image, Post, Tag

User = get_user_model()


class SeedDataCommandTests(TestCase):
    @patch('seed.management.commands.seed_data.PilImage.new')
    @patch('seed.management.commands.seed_data.generate_thumbnail')
    def test_seed_creates_users_posts_images_tags(
            self, mock_generate_thumbnail, mock_pil_new
    ):
        mock_pil_new.return_value = mock_pil_new
        mock_pil_new.save = lambda *args, **kwargs: None

        mock_thumbnail_file = BytesIO(b"fake image data")
        mock_thumbnail_file.name = 'path/to/thumbnail.jpg'

        mock_generate_thumbnail.return_value = mock_thumbnail_file

        call_command('seed_data')

        self.assertGreaterEqual(User.objects.count(), 5)
        self.assertGreaterEqual(Post.objects.count(), 5)
        self.assertGreaterEqual(Image.objects.count(), 5)
        self.assertGreaterEqual(Tag.objects.count(), 1)

    @patch('seed.management.commands.seed_data.PilImage.new')
    def test_seed_clear_removes_fake_data(self, mock_pil_new):
        user = User.objects.create_user(
            username='user0', email='user0@example.com', password='pass')
        post = Post.objects.create(author=user, caption='Test')
        tag = Tag.objects.create(name='testtag')
        post.tags.add(tag)

        self.assertEqual(User.objects.count(), 1)
        self.assertEqual(Post.objects.count(), 1)
        self.assertEqual(Tag.objects.count(), 1)

        call_command('seed_data', clear=True)

        self.assertEqual(User.objects.count(), 0)
        self.assertEqual(Post.objects.count(), 0)
        self.assertEqual(Tag.objects.count(), 0)

    @patch('seed.management.commands.seed_data.PilImage.new')
    def test_seed_clear_only_mode(self, mock_pil_new):
        user = User.objects.create_user(
            username='user0', email='user0@example.com', password='pass')
        post = Post.objects.create(author=user, caption='Test')
        tag = Tag.objects.create(name='testtag')
        post.tags.add(tag)

        self.assertEqual(User.objects.count(), 1)

        call_command('seed_data', clear=True)

        self.assertEqual(User.objects.count(), 0)
