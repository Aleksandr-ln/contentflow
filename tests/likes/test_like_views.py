from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from likes.models import Like
from posts.models import Post

User = get_user_model()


class LikeToggleTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='likeuser',
            email='likeuser@example.com',
            password='strongpassword987',
            is_active=True
        )
        self.post = Post.objects.create(
            author=self.user,
            caption='Post for like testing'
        )

    def test_like_and_unlike_post(self):
        self.client.login(email='likeuser@example.com',
                          password='strongpassword987')

        url = reverse('like-toggle-ajax')

        response = self.client.post(
            url,
            {'post_id': self.post.id},
            HTTP_X_REQUESTED_WITH='XMLHttpRequest'
        )
        self.assertEqual(response.status_code, 200)
        self.assertTrue(Like.objects.filter(
            user=self.user, post=self.post).exists())

        data = response.json()
        self.assertTrue(data['liked'])
        self.assertEqual(data['likes_count'], 1)

        response = self.client.post(
            url,
            {'post_id': self.post.id},
            HTTP_X_REQUESTED_WITH='XMLHttpRequest'
        )
        self.assertEqual(response.status_code, 200)
        self.assertFalse(Like.objects.filter(
            user=self.user, post=self.post).exists())

        data = response.json()
        self.assertFalse(data['liked'])
        self.assertEqual(data['likes_count'], 0)

    def test_like_toggle_missing_post_id(self):
        self.client.login(email='likeuser@example.com',
                          password='strongpassword987')
        url = reverse('like-toggle-ajax')

        response = self.client.post(
            url, {}, HTTP_X_REQUESTED_WITH='XMLHttpRequest')

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json()['error'], 'post_id is required')

    def test_like_toggle_invalid_post_id(self):
        self.client.login(email='likeuser@example.com',
                          password='strongpassword987')
        url = reverse('like-toggle-ajax')

        response = self.client.post(
            url, {'post_id': 9999}, HTTP_X_REQUESTED_WITH='XMLHttpRequest')

        self.assertEqual(response.status_code, 404)

    def test_like_toggle_unauthenticated(self):
        url = reverse('like-toggle-ajax')

        response = self.client.post(
            url,
            {'post_id': self.post.id},
            HTTP_X_REQUESTED_WITH='XMLHttpRequest',
        )

        self.assertEqual(response.status_code, 302)

    def test_like_toggle_invalid_request_type(self):
        self.client.login(email='likeuser@example.com',
                          password='strongpassword987')
        url = reverse('like-toggle-ajax')

        # без HTTP_X_REQUESTED_WITH
        response = self.client.post(url, {'post_id': self.post.id})

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json()['error'], 'Invalid request type')
