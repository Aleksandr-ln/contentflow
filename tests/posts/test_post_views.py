from io import BytesIO

from django.contrib.auth import get_user_model
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase
from django.urls import reverse
from PIL import Image as PILImage

from posts.models import Post, Tag

User = get_user_model()


class PostViewsTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='postuser',
            email='postuser@example.com',
            password='strongpassword789',
            is_active=True
        )
        self.client.login(email='postuser@example.com',
                          password='strongpassword789')

    def create_test_image(self):
        img = PILImage.new('RGB', (100, 100), color='blue')
        buffer = BytesIO()
        img.save(buffer, format='JPEG')
        buffer.seek(0)
        return SimpleUploadedFile(
            'test_image.jpg',
            buffer.read(),
            content_type='image/jpeg',
        )

    def test_create_post_with_tags_and_images(self):
        url = reverse('post-create')

        image_files = {
            f'form-{i}-image': self.create_test_image()
            for i in range(3)
        }

        data = {
            'caption': 'This is a test post with #testtag1 and #TestTag2',
            'form-TOTAL_FORMS': '5',
            'form-INITIAL_FORMS': '0',
        }

        response = self.client.post(
            url, {**data, **image_files}, format='multipart')
        self.assertEqual(response.status_code, 302)

        post = Post.objects.first()
        self.assertIsNotNone(post)
        self.assertEqual(
            post.caption, 'This is a test post with #testtag1 and #TestTag2')

        tags = post.tags.all()
        tag_names = [tag.name for tag in tags]
        self.assertIn('testtag1', tag_names)
        self.assertIn('testtag2', tag_names)

        images = post.images.all()
        self.assertEqual(images.count(), 3)

    def test_post_list_view_shows_posts(self):
        Post.objects.create(author=self.user, caption="Visible post")
        url = reverse('post-list')
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Visible post")

    def test_post_list_by_tag_filters_posts(self):
        tag = Tag.objects.create(name='filteredtag')
        post = Post.objects.create(author=self.user, caption="Filtered post")
        post.tags.add(tag)

        url = reverse('post-by-tag', kwargs={'tag_name': 'filteredtag'})
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Filtered post")

    def test_post_update_view_updates_caption(self):
        post = Post.objects.create(author=self.user, caption="Old caption")
        url = reverse('post-edit', kwargs={'pk': post.id})

        data = {
            'caption': 'Updated caption',
            'form-TOTAL_FORMS': '1',
            'form-INITIAL_FORMS': '0',
        }

        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 302)

        post.refresh_from_db()
        self.assertEqual(post.caption, 'Updated caption')

    def test_post_delete_view_deletes_post(self):
        post = Post.objects.create(author=self.user, caption="To be deleted")
        url = reverse('post-delete', kwargs={'pk': post.id})

        response = self.client.post(url)
        self.assertEqual(response.status_code, 302)

        self.assertFalse(Post.objects.filter(id=post.id).exists())
