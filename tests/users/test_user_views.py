from django.contrib.auth import get_user_model
from django.contrib.auth.tokens import default_token_generator
from django.test import TestCase
from django.urls import reverse
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode

from posts.models import Post

User = get_user_model()


class UserRegistrationTests(TestCase):
    def test_user_registration_flow(self):
        response = self.client.post(reverse('users:register'), {
            'username': 'testuser',
            'email': 'testuser@example.com',
            'password': 'strongpassword123',
            'password_confirm': 'strongpassword123'
        })

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'users/confirm_email_sent.html')

        user_exists = User.objects.filter(
            email='testuser@example.com').exists()
        self.assertTrue(user_exists)

        user = User.objects.get(email='testuser@example.com')
        self.assertFalse(user.is_active)

    def test_register_view_get(self):
        url = reverse('users:register')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'users/register.html')


class UserActivationTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser2',
            email='testuser2@example.com',
            password='strongpassword456',
            is_active=False
        )

    def test_user_activation_flow(self):
        uid = urlsafe_base64_encode(force_bytes(self.user.pk))
        token = default_token_generator.make_token(self.user)
        activation_url = reverse(
            'users:activate', kwargs={'uidb64': uid, 'token': token})

        response = self.client.get(activation_url)

        self.user.refresh_from_db()
        self.assertEqual(response.status_code, 302)
        self.assertTrue(self.user.is_active)


class ProfileViewTests(TestCase):
    def setUp(self):
        self.user = self.create_user('testuser@example.com')
        self.other_user = self.create_user('otheruser@example.com')

        self.post1 = Post.objects.create(
            author=self.user, caption="User's post 1")
        self.post2 = Post.objects.create(
            author=self.user, caption="User's post 2")

    def create_user(self, email):
        from django.contrib.auth import get_user_model
        User = get_user_model()
        return User.objects.create_user(
            username=email.split('@')[0],
            email=email,
            password='pass123'
        )


class ProfileEditViewTests(TestCase):
    def setUp(self):
        self.user = self.create_user('edituser@example.com')
        self.other_user = self.create_user('viewer@example.com')

    def create_user(self, email):
        from django.contrib.auth import get_user_model
        User = get_user_model()
        return User.objects.create_user(
            username=email.split('@')[0],
            email=email,
            password='pass123'
        )

    def test_profile_edit_success(self):
        self.client.login(email='edituser@example.com', password='pass123')

        url = reverse('users:profile-edit',
                      kwargs={'username': self.user.username})
        response = self.client.post(url, {
            'full_name': 'Updated Name',
            'bio': 'Updated Bio'
        })

        self.assertEqual(response.status_code, 302)
        self.user.refresh_from_db()
        self.assertEqual(self.user.full_name, 'Updated Name')
        self.assertEqual(self.user.bio, 'Updated Bio')

    def test_profile_edit_forbidden_for_other_user(self):
        self.client.login(email='viewer@example.com', password='pass123')

        url = reverse('users:profile-edit',
                      kwargs={'username': self.user.username})
        response = self.client.post(url, {
            'full_name': 'Hack Attempt',
        })

        self.assertEqual(response.status_code, 403)


class RedirectToOwnProfileTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            email='testuser@example.com',
            password='pass123'
        )

    def test_redirect_to_own_profile(self):
        self.client.login(email='testuser@example.com', password='pass123')
        url = reverse('users:my-profile')
        response = self.client.get(url)
        self.assertRedirects(response, reverse(
            'users:profile', kwargs={'username': 'testuser'}))
