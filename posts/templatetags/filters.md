# Custom Template Filters – `post_tags.py`

This module contains custom template filters used in the `posts` application to process text and hashtags in templates.

---

## Tag Filters

| Filter | Description |
|--------|-------------|
| `linkify_hashtags(text)` | Converts hashtags (e.g. `#django`) into clickable links: `<a href="/posts/tag/django/">#django</a>`. Also replaces `\n` with `<br>`. |
| `remove_hashtags(text)` | Removes all hashtags from the text. Supports Cyrillic and Latin hashtags. |
| `extract_hashtags(text)` | Extracts a list of unique hashtags from the text in the order they appear. |

---

## Text Filters

| Filter | Description |
|--------|-------------|
| `split(value, delimiter=" ")` | Splits a string by the given delimiter (default: space). Useful in templates for basic list generation. |
| `remove_trailing_newlines(text)` | Removes trailing line breaks, carriage returns, tabs, and spaces from the end of the string. |
