from typing import Optional

from django import forms
from django.contrib.auth.models import AbstractBaseUser
from django.forms.widgets import FileInput

from posts.services.tag_services import update_post_tags

from .models import Image, Post


class PostForm(forms.ModelForm):
    """
    Form for creating and updating posts with
    caption and auto-extracted hashtags.

    The form supports assigning an author and processes tags
    automatically during save() via the update_post_tags service.
    """

    class Meta:
        model = Post
        fields = ['caption']
        widgets = {
            'caption': forms.Textarea(attrs={
                'placeholder': 'Add caption and hashtags...',
            })
        }
        labels = {
            'caption': ''
        }

    def save(
            self,
            author: Optional[AbstractBaseUser] = None,
            commit: bool = True) -> Post:
        """
        Save the post instance with optional
        author assignment and tag extraction.

        Args:
            author (AbstractBaseUser | None):
            Optional author to assign to the post.
            commit (bool):
            Whether to save the post to the database immediately.

        Returns:
            Post: The saved Post instance.
        """
        post = super().save(commit=False)

        if author:
            post.author = author

        if commit:
            post.save()
            update_post_tags(post, post.caption)
        return post


class ImageForm(forms.ModelForm):
    """
    Form for uploading or editing a single image in a post.
    """
    image = forms.ImageField(required=False, widget=FileInput)

    class Meta:
        model = Image
        fields = ['id', 'image']
