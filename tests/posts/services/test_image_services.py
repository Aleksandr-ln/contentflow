import io

from django.core.files.uploadedfile import SimpleUploadedFile
from django.forms import modelformset_factory
from django.test import TestCase

from posts.forms import ImageForm
from posts.models import Image, Post
from posts.services.image_services import (handle_images_update,
                                           save_images_to_post)


class SaveImagesToPostTests(TestCase):
    def setUp(self):
        self.post = Post.objects.create(
            author=self.create_user(),
            caption="Test post"
        )

    def create_user(self):
        from django.contrib.auth import get_user_model
        User = get_user_model()
        return User.objects.create_user(
            username='testuser',
            email='testuser@example.com',
            password='testpass123'
        )

    def create_test_image_file(self, name='test.jpg') -> SimpleUploadedFile:
        img_bytes = io.BytesIO()
        from PIL import Image as PilImage
        img = PilImage.new('RGB', (100, 100), color='red')
        img.save(img_bytes, format='JPEG')
        img_bytes.seek(0)
        return SimpleUploadedFile(
            name, img_bytes.read(),
            content_type='image/jpeg'
        )

    def test_save_images_to_post(self):
        images_data = [{'image': self.create_test_image_file()}
                       for _ in range(2)]

        save_images_to_post(self.post, images_data)

        self.assertEqual(self.post.images.count(), 2)
        for img in self.post.images.all():
            self.assertTrue(img.thumbnail.name.startswith(
                'posts/thumbnails/thumb_'))

    def test_save_images_to_post_ignores_empty_data(self):
        images_data = [
            {'image': self.create_test_image_file()},
            {},
            None
        ]

        save_images_to_post(self.post, images_data)

        self.assertEqual(self.post.images.count(), 1)


class HandleImagesUpdateTests(TestCase):
    def setUp(self):
        self.post = Post.objects.create(
            author=self.create_user(),
            caption="Test post"
        )
        self.image1 = Image.objects.create(post=self.post, image='test1.jpg')
        self.image2 = Image.objects.create(post=self.post, image='test2.jpg')

    def create_user(self):
        from django.contrib.auth import get_user_model
        User = get_user_model()
        return User.objects.create_user(
            username='testuser',
            email='testuser@example.com',
            password='testpass123'
        )

    def test_handle_images_update_deletes_marked_images(self):
        ImageFormSet = modelformset_factory(
            Image, form=ImageForm, can_delete=True)

        form_data = {
            'form-TOTAL_FORMS': '2',
            'form-INITIAL_FORMS': '2',
            'form-0-id': str(self.image1.id),
            'form-0-DELETE': 'on',
            'form-1-id': str(self.image2.id),
        }

        formset = ImageFormSet(form_data, queryset=self.post.images.all())

        self.assertTrue(formset.is_valid())

        handle_images_update(self.post, formset)

        remaining_images = self.post.images.all()
        self.assertEqual(remaining_images.count(), 1)
        self.assertEqual(remaining_images.first().id, self.image2.id)

    def test_handle_images_update_generates_thumbnail_if_missing(self):
        self.image1.thumbnail = None
        self.image1.save()

        ImageFormSet = modelformset_factory(
            Image, form=ImageForm, can_delete=True)
        form_data = {
            'form-TOTAL_FORMS': '2',
            'form-INITIAL_FORMS': '2',
            'form-0-id': str(self.image1.id),
            'form-1-id': str(self.image2.id),
        }

        formset = ImageFormSet(form_data, queryset=self.post.images.all())

        self.assertTrue(formset.is_valid())

        handle_images_update(self.post, formset)

        updated_image = Image.objects.get(id=self.image1.id)
        self.assertIsNotNone(updated_image.thumbnail)
