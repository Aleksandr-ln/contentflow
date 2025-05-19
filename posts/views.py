"""
posts/views.py

This module handles views related to post operations in ContentFlow.
It includes:
- Displaying a feed of posts from other users
- Creating a post with multiple images and tags
"""

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.core.paginator import Paginator
from django.forms import modelformset_factory
from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect, render
from django.urls import reverse
from django.views.generic import DeleteView
from django.views.generic.edit import UpdateView

from posts.services.image_services import (handle_images_update,
                                           save_images_to_post)
from posts.services.selectors import (get_post_feed_for_user,
                                      get_posts_by_tag_for_user)
from posts.services.tag_services import update_post_tags

from .forms import ImageForm, PostForm
from .models import Image, Post


@login_required
def post_list_view(request: HttpRequest) -> HttpResponse:
    """
    Feed of latest posts.

    Args:
        request (HttpRequest): The HTTP request object.

    Returns:
        HttpResponse: Rendered template with filtered posts.
    """
    posts_qs = get_post_feed_for_user(request.user)

    paginator = Paginator(posts_qs, 5)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'posts/list.html', {
        'page_obj': page_obj,
        'posts': page_obj.object_list,
    })


@login_required
def post_create_view(request: HttpRequest) -> HttpResponse:
    """
    Create a post with up to 5 images and tags.

    Args:
        request (HttpRequest): The HTTP request object.

    Returns:
        HttpResponse: Redirects to post feed if successful,
        otherwise renders form with errors.
    """
    ImageFormSet = modelformset_factory(
        Image,
        form=ImageForm,
        extra=5,
        max_num=5,
        validate_max=True
    )

    if request.method == 'POST':
        post_form = PostForm(request.POST)
        formset = ImageFormSet(
            request.POST,
            request.FILES,
            queryset=Image.objects.none())

        if post_form.is_valid() and formset.is_valid():
            post = post_form.save(author=request.user)
            save_images_to_post(post, formset.cleaned_data)

            messages.success(request, "Post was created successfully!")
            return redirect('post-list')

        print("Formset or post_form errors:")
        print(post_form.errors)
        print(formset.errors)

    else:
        post_form = PostForm()
        formset = ImageFormSet(queryset=Image.objects.none())

    return render(request, 'posts/create.html', {
        'post_form': post_form,
        'formset': formset
    })


@login_required
def post_list_by_tag(request: HttpRequest, tag_name: str) -> HttpResponse:
    """
    Display posts filtered by tag.
    """
    posts_qs = get_posts_by_tag_for_user(request.user, tag_name)

    paginator = Paginator(posts_qs, 5)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'posts/list.html', {
        'page_obj': page_obj,
        'posts': page_obj.object_list,
        'filter_tag': tag_name,
    })


ImageFormSet = modelformset_factory(
    Image,
    form=ImageForm,
    extra=5,
    can_delete=True,
    validate_max=True,
    min_num=1,
    max_num=5,
    absolute_max=5
)


class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    form_class = PostForm
    template_name = 'posts/edit.html'

    def get_success_url(self) -> str:
        """
        Return the URL to redirect to after successful post update.
        """
        return reverse('users:profile', args=[self.request.user.username])

    def test_func(self) -> bool:
        """
        Check whether the currently logged-in user is the author of the post.
        """
        post = self.get_object()
        return post.author == self.request.user

    def get_context_data(self, **kwargs: object) -> dict:
        """
        Add image formset to the context for both GET and POST requests.

        Returns:
            dict: The context dictionary with formset included.
        """
        context = super().get_context_data(**kwargs)
        if self.request.method == 'POST':
            context['formset'] = ImageFormSet(
                self.request.POST,
                self.request.FILES,
                queryset=self.object.images.all())
        else:
            context['formset'] = ImageFormSet(
                queryset=self.object.images.all())
        return context

    def post(
            self,
            request: HttpRequest,
            *args: object,
            **kwargs: object) -> HttpResponse:
        """
        Handle the POST request for editing a post with
        multiple images and tags.

        Returns:
            HttpResponse: Redirects to the user's profile on success,
            or re-renders the form with validation errors.
        """
        self.object = self.get_object()
        form = self.get_form()
        formset = ImageFormSet(
            request.POST,
            request.FILES,
            queryset=self.object.images.all())

        if not formset.is_valid() or not form.is_valid():
            return self.render_to_response(
                self.get_context_data(
                    form=form, formset=formset))

        post = form.save(commit=False)
        post.author = request.user
        post.save()

        update_post_tags(post, post.caption)

        handle_images_update(post, formset)

        return redirect(self.get_success_url())


class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    """
    View for deleting a post. Only the author of the post can delete it.
    """
    model = Post
    template_name = "posts/confirm_delete.html"

    def get_success_url(self) -> str:
        """
        Return the URL to redirect to after successful post delete.
        """
        return reverse('users:profile', args=[self.request.user.username])

    def test_func(self) -> bool:
        """
        Ensure that only the author can delete their post.
        """
        post = self.get_object()
        return self.request.user == post.author
