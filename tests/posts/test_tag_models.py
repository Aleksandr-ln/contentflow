from django.db import IntegrityError
from django.test import TestCase

from posts.models import Tag


class TagModelTests(TestCase):
    def test_tag_is_lowercased_on_save(self) -> None:
        """Tag.save must normalize 'name' to lowercase."""
        t = Tag.objects.create(name="  PyThOn ")
        self.assertEqual(t.name, "python")

    def test_tag_case_insensitive_unique(self) -> None:
        """DB must reject duplicates regardless of letter case."""
        Tag.objects.create(name="django")
        with self.assertRaises(IntegrityError):
            Tag.objects.create(name="Django")
