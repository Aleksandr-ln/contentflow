import re
from typing import List

from posts.models import Post, Tag


def extract_tag_names(tag_input: str) -> List[str]:
    """
    Extract hashtag names from a string.

    This function parses hashtags from a string such as "#Python #Django"
    and returns a list of lowercase tag names without the hash symbol.

    Args:
        tag_input (str): A string containing hashtags.

    Returns:
        List[str]: A list of tag names in lowercase.
    """
    return [
        tag.lower() for tag in re.findall(
            r"#([\wа-яА-ЯёЁїЇіІєЄґҐ]+)",
            tag_input,
            flags=re.UNICODE)]


def update_post_tags(post: Post, caption: str) -> None:
    """
    Clear and update tags for a post based on its caption.

    This ensures tags in the DB match the current state of the post.
    """
    post.tags.clear()
    for tag_name in extract_tag_names(caption):
        tag, _ = Tag.objects.get_or_create(name=tag_name)
        post.tags.add(tag)
