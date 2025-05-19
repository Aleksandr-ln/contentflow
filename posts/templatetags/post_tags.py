import re
from typing import List

from django import template
from django.utils.safestring import mark_safe

register = template.Library()


@register.filter
def linkify_hashtags(text: str) -> str:
    """
    Converts hashtags in text to clickable links and preserves line breaks.
    Example: #python → <a href="/posts/tag/python/">#python</a>
    Also replaces \n with <br> for display purposes.
    """
    if not text:
        return ""

    def replace_tag(match):
        """
        Replace a regex match object with an HTML anchor tag for the hashtag.

        Args:
            match (re.Match): The match object containing the hashtag text.

        Returns:
            str: HTML string representing a clickable hashtag link.
        """
        tag = match.group(1)
        url = f'/posts/tag/{tag}/'
        return f'<a href="{url}">#{tag}</a>'

    linked_text = re.sub(
        r'#([\wа-яА-ЯёЁїЇіІєЄґҐ]+)',
        replace_tag,
        text,
        flags=re.UNICODE)
    linked_text = linked_text.replace('\n', '<br>')
    return mark_safe(linked_text)


@register.filter
def split(value: str, delimiter: str = " ") -> List[str]:
    """
    Splits a string by the given delimiter (default: space).
    Usage: {{ value|split:"," }}
    """
    if not value:
        return []
    return value.split(delimiter)


@register.filter
def remove_hashtags(text: str) -> str:
    """Removes hashtags from a string."""
    if not text:
        return ""
    return re.sub(r"#([\wа-яА-ЯёЁїЇіІєЄґҐ]+)", "", text, flags=re.UNICODE)


@register.filter
def extract_hashtags(text: str) -> List[str]:
    """
    Returns a list of unique hashtags in the order in which they appear.
    """
    if not text:
        return []
    seen = set()
    tags = []
    for tag in re.findall(r"#\w+", text):
        if tag not in seen:
            seen.add(tag)
            tags.append(tag)
    return tags


@register.filter
def remove_trailing_newlines(text: str) -> str:
    """
    Remove trailing line breaks, carriage returns and
    spaces to avoid layout gaps.
    """
    if not text:
        return ""
    return text.rstrip("\n\r\t ")
