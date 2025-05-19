from django.contrib.auth import get_user_model
from django.test import TestCase

User = get_user_model()


class UserModelTests(TestCase):
    def test_user_str(self):
        user = User.objects.create_user(
            username='testuser',
            email='testuser@example.com',
            password='testpass123'
        )

        self.assertEqual(str(user), 'testuser@example.com')

    def test_email_must_be_unique(self):
        User.objects.create_user(
            username='user1', email='unique@example.com', password='pass')
        with self.assertRaises(Exception):
            User.objects.create_user(
                username='user2', email='unique@example.com', password='pass')

    def test_username_field_is_email(self):
        self.assertEqual(User.USERNAME_FIELD, 'email')

    def test_user_avatar_upload(self):
        from django.core.files.uploadedfile import SimpleUploadedFile

        avatar = SimpleUploadedFile(
            name='avatar.jpg',
            content=b'file_content',
            content_type='image/jpeg'
        )
        user = User.objects.create_user(
            username='avataruser',
            email='avatar@example.com',
            password='pass',
            avatar=avatar
        )

        self.assertTrue(user.avatar.name.startswith('avatars/'))
