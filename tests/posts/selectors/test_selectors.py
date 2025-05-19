from django.test import TestCase

from likes.models import Like
from posts.models import Post, Tag
from posts.services.selectors import (get_post_feed_for_user,
                                      get_posts_by_tag_for_user,
                                      get_posts_by_user)


class GetPostFeedForUserTests(TestCase):
    def setUp(self):
        self.user = self.create_user('feeduser@example.com')
        self.other_user = self.create_user('other@example.com')

        self.post1 = Post.objects.create(
            author=self.other_user, caption="Post 1")
        self.post2 = Post.objects.create(
            author=self.other_user, caption="Post 2")

        Like.objects.create(user=self.user, post=self.post1)

    def create_user(self, email):
        from django.contrib.auth import get_user_model
        User = get_user_model()
        return User.objects.create_user(
            username=email.split('@')[0],
            email=email,
            password='pass123'
        )

    def test_get_post_feed_with_likes(self):
        qs = get_post_feed_for_user(self.user)

        self.assertEqual(qs.count(), 2)

        post1 = qs.get(id=self.post1.id)
        post2 = qs.get(id=self.post2.id)

        self.assertEqual(post1.likes_count, 1)
        self.assertEqual(post2.likes_count, 0)

        self.assertTrue(post1.has_liked)
        self.assertFalse(post2.has_liked)


class GetPostsByTagForUserTests(TestCase):
    def setUp(self):
        self.user = self.create_user('taguser@example.com')

        self.post1 = Post.objects.create(
            author=self.user, caption="Post with #tag1")
        self.post2 = Post.objects.create(
            author=self.user, caption="Post with #tag2")

        self.tag1 = Tag.objects.create(name='tag1')
        self.tag2 = Tag.objects.create(name='tag2')

        self.post1.tags.add(self.tag1)
        self.post2.tags.add(self.tag2)

    def create_user(self, email):
        from django.contrib.auth import get_user_model
        User = get_user_model()
        return User.objects.create_user(
            username=email.split('@')[0],
            email=email,
            password='pass123'
        )

    def test_get_posts_by_tag(self):
        qs = get_posts_by_tag_for_user(self.user, 'tag1')

        self.assertEqual(qs.count(), 1)
        self.assertEqual(qs.first().id, self.post1.id)

    def test_get_posts_by_tag_returns_empty_if_not_found(self):
        qs = get_posts_by_tag_for_user(self.user, 'nonexistent')
        self.assertEqual(qs.count(), 0)


class GetPostsByUserTests(TestCase):
    def setUp(self):
        self.user = self.create_user('author@example.com')
        self.viewer = self.create_user('viewer@example.com')

        self.post1 = Post.objects.create(author=self.user, caption="Post 1")
        self.post2 = Post.objects.create(author=self.user, caption="Post 2")

    def create_user(self, email):
        from django.contrib.auth import get_user_model
        User = get_user_model()
        return User.objects.create_user(
            username=email.split('@')[0],
            email=email,
            password='pass123'
        )

    def test_get_posts_by_user(self):
        qs = get_posts_by_user(self.user, self.viewer)

        self.assertEqual(qs.count(), 2)
        self.assertIn(self.post1, qs)
        self.assertIn(self.post2, qs)

    def test_get_posts_by_user_no_posts(self):
        new_user = self.create_user('new@example.com')
        qs = get_posts_by_user(new_user, self.user)
        self.assertEqual(qs.count(), 0)
