from django import template

register = template.Library()


@register.filter
def normalize_password_errors(errors: list[str]) -> str:
    """
    Normalize Django password validation messages
    into a human-friendly sentence.
    Handles both single and multiple cases grammatically.
    """
    if not errors:
        return ""

    replacements = {
        "This password is too short. It must contain at least 8 characters.": (
            "be at least 8 characters", False
        ),
        "This password is too common.": (
            "too common", True
        ),
        "This password is entirely numeric.": (
                "entirely numeric", True
        ),
    }

    parts = []
    for error in errors:
        replacement = replacements.get(error)
        if replacement:
            text, is_negative = replacement
            if is_negative:
                parts.append(f"not be {text}")
            else:
                parts.append(f"be {text}")
        else:
            parts.append(error)  # fallback

    if len(parts) == 1:
        return f"Password must {parts[0]}."
    else:
        return f"Password must {', '.join(parts[:-1])} and {parts[-1]}."
