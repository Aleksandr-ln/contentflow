from django.contrib.auth import get_user_model
from django.test import TestCase

from users.forms import UserRegisterForm

User = get_user_model()


class UserRegisterFormTests(TestCase):
    def test_passwords_must_match(self):
        form = UserRegisterForm(data={
            'username': 'testuser',
            'email': 'testuser@example.com',
            'password': 'password123',
            'password_confirm': 'differentpassword'
        })
        self.assertFalse(form.is_valid())
        self.assertIn('password_confirm', form.errors)
        self.assertEqual(form.errors['password_confirm']
                         [0], 'Passwords do not match.')

    def test_username_must_be_unique(self):
        User.objects.create_user(
            username='testuser', email='exists@example.com', password='pass')
        form = UserRegisterForm(data={
            'username': 'testuser',
            'email': 'new@example.com',
            'password': 'StrongPassword123!',
            'password_confirm': 'StrongPassword123!'
        })
        self.assertFalse(form.is_valid())
        self.assertIn('username', form.errors)
        self.assertEqual(form.errors['username'][0],
                         'This username is already taken.')

    def test_successful_registration(self):
        form = UserRegisterForm(data={
            'username': 'newuser',
            'email': 'newuser@example.com',
            'password': 'StrongPassword123!',
            'password_confirm': 'StrongPassword123!'
        })
        self.assertTrue(form.is_valid())

    def test_password_strength_validation(self):
        form = UserRegisterForm(data={
            'username': 'weakuser',
            'email': 'weak@example.com',
            'password': '123',
            'password_confirm': '123'
        })
        self.assertFalse(form.is_valid())
        self.assertIn('password', form.errors)
