from django.test import TestCase

from posts.models import Post, Tag
from posts.services.tag_services import extract_tag_names, update_post_tags


class ExtractTagNamesTests(TestCase):
    def test_extract_tags_correctly(self):
        text = "Learning #Python #Django #WebDev is fun! #PYTHON"
        expected_tags = ['python', 'django', 'webdev', 'python']

        result = extract_tag_names(text)

        self.assertEqual(result, expected_tags)

    def test_no_hashtags(self):
        text = "This text has no hashtags."
        result = extract_tag_names(text)
        self.assertEqual(result, [])


class UpdatePostTagsTests(TestCase):
    def setUp(self):
        from django.contrib.auth import get_user_model
        User = get_user_model()
        self.user = User.objects.create_user(
            username='testuser',
            email='testuser@example.com',
            password='pass123'
        )
        self.post = Post.objects.create(author=self.user, caption="")

    def test_update_post_tags_adds_and_clears(self):
        old_tag = Tag.objects.create(name='oldtag')
        self.post.tags.add(old_tag)

        caption = "This is a new #Python #Django post"
        update_post_tags(self.post, caption)

        tag_names = set(self.post.tags.values_list('name', flat=True))

        self.assertIn('python', tag_names)
        self.assertIn('django', tag_names)
        self.assertNotIn('oldtag', tag_names)

        self.assertTrue(Tag.objects.filter(name='python').exists())
        self.assertTrue(Tag.objects.filter(name='django').exists())
