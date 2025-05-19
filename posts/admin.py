from django.contrib import admin
from django.utils.html import format_html

from .models import Image, Post, Tag


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    """
    Admin configuration for the Post model.
    Includes display of author, caption, tags, and created time.
    """
    list_display = ('author', 'caption', 'tag_list', 'created_at')
    list_filter = ('created_at', 'tags')
    search_fields = ('caption', 'author__username')

    def tag_list(self, obj):
        """
        Return a comma-separated list of tag names associated with the post.
        """
        return ", ".join(tag.name for tag in obj.tags.all())
    tag_list.short_description = "Tags"


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    """
    Admin configuration for the Tag model.
    Enables searching by tag name.
    """
    search_fields = ('name',)


@admin.register(Image)
class ImageAdmin(admin.ModelAdmin):
    """
    Admin configuration for the Image model.
    Displays image and thumbnail preview in the list view.
    """
    list_display = ('post', 'image', 'thumbnail_preview')

    def thumbnail_preview(self, obj):
        """
        Display an HTML <img> tag with the thumbnail, or '-' if missing.
        """
        if obj.thumbnail:
            return format_html(
                '<img src="{}" width="100" '
                'style="object-fit:contain; border-radius:4px;">',
                obj.thumbnail.url)
        return "-"
    thumbnail_preview.short_description = "Thumbnail"
