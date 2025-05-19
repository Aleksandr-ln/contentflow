from django.test import TestCase

from posts.templatetags.post_tags import (extract_hashtags, linkify_hashtags,
                                          remove_hashtags,
                                          remove_trailing_newlines, split)


class LinkifyHashtagsTests(TestCase):
    def test_convert_hashtags_to_links(self):
        text = "This is a #test and another #ExampleTag"
        expected = (
            'This is a '
            '<a href="/posts/tag/test/">#test</a> '
            'and another '
            '<a href="/posts/tag/ExampleTag/">#ExampleTag</a>'
        )

        result = linkify_hashtags(text)
        self.assertEqual(result, expected)

    def test_text_without_hashtags(self):
        text = "No hashtags here."
        result = linkify_hashtags(text)
        self.assertEqual(result, text)


class PostTagsFilterTests(TestCase):
    def test_split_default_delimiter(self):
        self.assertEqual(split("one two three"), ["one", "two", "three"])

    def test_split_custom_delimiter(self):
        self.assertEqual(split("a,b,c", ","), ["a", "b", "c"])

    def test_split_empty_value(self):
        self.assertEqual(split("", ","), [])

    def test_remove_hashtags(self):
        self.assertEqual(remove_hashtags("Hello #world!"), "Hello !")
        self.assertEqual(remove_hashtags("#one #two"), " ")
        self.assertEqual(remove_hashtags("No tags here"), "No tags here")

    def test_extract_hashtags(self):
        self.assertEqual(extract_hashtags("#one #two #one"), ["#one", "#two"])
        self.assertEqual(extract_hashtags("Text with #tag"), ["#tag"])
        self.assertEqual(extract_hashtags("No hashtags"), [])

    def test_remove_trailing_newlines(self):
        self.assertEqual(remove_trailing_newlines("Line\n\n"), "Line")
        self.assertEqual(remove_trailing_newlines("Text \r\t "), "Text")
        self.assertEqual(remove_trailing_newlines("Clean text"), "Clean text")
