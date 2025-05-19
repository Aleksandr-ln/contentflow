from io import BytesIO
from pathlib import Path

from django.core.files.base import ContentFile
from PIL import Image as PilImage

THUMBNAIL_SIZE = (300, 300)


def generate_thumbnail(original_image_field) -> ContentFile:
    """
    Generate thumbnail for an uploaded image and return as ContentFile.
    """
    img = PilImage.open(original_image_field)

    if img.mode in ("RGBA", "P"):
        img = img.convert("RGB")

    img.thumbnail(THUMBNAIL_SIZE)

    thumb_io = BytesIO()
    img.save(thumb_io, format="JPEG", quality=85)

    filename = Path(original_image_field.name).name
    thumb_filename = f"thumb_{filename}"

    return ContentFile(thumb_io.getvalue(), name=thumb_filename)
