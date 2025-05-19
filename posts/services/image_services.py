from typing import Any

from django.core.files.uploadedfile import UploadedFile
from django.forms import BaseModelFormSet

from posts.models import Image, Post
from posts.services.image_utils import generate_thumbnail


def save_images_to_post(post: Post, images_data: list[dict[str, Any]]) -> None:
    """
    Save images to a given post based on cleaned formset data.

    Each dictionary in images_data represents one cleaned form's data.
    If the image field is present, it creates a new Image instance linked
    to the post and generates a thumbnail for it.

    Args:
        post (Post): The post instance to associate images with.
        images_data (list[dict[str, Any]]): Cleaned data from an image formset.
    """
    for form_data in images_data:
        if not form_data or not form_data.get("image"):
            continue

        original: UploadedFile = form_data["image"]
        image_obj = Image.objects.create(post=post, image=original)

        thumb = generate_thumbnail(original)
        image_obj.thumbnail.save(thumb.name, thumb, save=True)


def handle_images_update(post: Post, formset: BaseModelFormSet) -> None:
    """
    Handle adding, updating, and deleting images
    related to a given post using a formset.

    This function processes the formset:
    - Saves new or updated images linked to the post
    - Ensures that a thumbnail is generated for each image (if missing)
    - Deletes any images marked for deletion via the formset

    Args:
        post (Post): The post instance to associate images with.
        formset (BaseModelFormSet): The formset containing ImageForm data.
    """
    images = formset.save(commit=False)

    for image in images:
        if image.image:
            image.post = post
            image.save()

            if not image.thumbnail:
                thumb = generate_thumbnail(image.image)
                image.thumbnail.save(thumb.name, thumb, save=True)

    for obj in formset.deleted_objects:
        obj.delete()
