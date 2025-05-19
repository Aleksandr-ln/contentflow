"""
Views for user registration, profile viewing, profile editing,
and account activation via email confirmation in the ContentFlow application.
"""

from django.contrib import messages
from django.contrib.auth import get_user_model, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import AbstractBaseUser
from django.contrib.auth.tokens import default_token_generator
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import EmailMultiAlternatives
from django.core.paginator import Paginator
from django.http import HttpRequest, HttpResponse, HttpResponseForbidden
from django.shortcuts import get_object_or_404, redirect, render
from django.template.loader import render_to_string
from django.urls import reverse
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode

from posts.services.selectors import get_posts_by_user

from .forms import ProfileUpdateForm, UserRegisterForm


def send_activation_email(
        user: AbstractBaseUser,
        activation_link: str) -> None:
    """
    Send a confirmation email to the user with the provided activation link.

    Args:
        user (User): The user who registered and needs activation.
        activation_link (str): The full activation URL to include in the email.
    """
    subject = 'Confirm your ContentFlow account'
    from_email = 'admin@contentflow.local'
    to_email = [user.email]

    text_content = f'Please click the link to activate: {activation_link}'
    html_content = render_to_string(
        'users/activation_email.html', {'activation_link': activation_link})

    email = EmailMultiAlternatives(subject, text_content, from_email, to_email)
    email.attach_alternative(html_content, "text/html")
    email.send()


def register_view(request: HttpRequest) -> HttpResponse:
    """
    Display the registration form and process form submissions.

    - If the request method is GET, renders the form.
    - If POST and valid, creates an inactive user and sends activation email.

    Args:
        request (HttpRequest): The incoming request object.

    Returns:
        HttpResponse: The rendered form page or redirect after success.
    """
    if request.method == "POST":
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data["password"])
            user.is_active = False
            user.save()

            token = default_token_generator.make_token(user)
            uid = urlsafe_base64_encode(force_bytes(user.pk))
            domain = get_current_site(request).domain
            link = reverse(
                'users:activate', kwargs={
                    'uidb64': uid, 'token': token})
            activate_url = f'http://{domain}{link}'

            send_activation_email(user, activate_url)
            messages.info(
                request,
                "Confirmation email sent. Please check your inbox.")
            return render(request, 'users/confirm_email_sent.html')

    else:
        form = UserRegisterForm()
    return render(request, 'users/register.html', {'form': form})


def activate_user(
        request: HttpRequest, uidb64: str, token: str
) -> HttpResponse:
    """
    Activate user via email confirmation link and
    redirect to profile or profile-edit.
    """
    User = get_user_model()
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except Exception:
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        user.is_active = True
        user.save()
        login(request, user)

        if not user.full_name and not user.avatar:
            return redirect('users:profile-edit', username=user.username)
        else:
            return redirect('users:profile', username=user.username)

    return render(request, 'users/activation_failed.html')


@login_required
def profile_view(request: HttpRequest, username: str) -> HttpResponse:
    """
    View-only version of a user profile. Allows viewing bio, avatar, and posts.
    Only the profile owner will see the link to edit their profile.
    """
    User = get_user_model()
    viewed_user = get_object_or_404(User, username=username)

    posts_qs = get_posts_by_user(viewed_user, request.user)

    paginator = Paginator(posts_qs, 5)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'users/profile.html', {
        'viewed_user': viewed_user,
        'page_obj': page_obj,
        'posts': page_obj.object_list,
    })


@login_required
def redirect_to_own_profile(request: HttpRequest) -> HttpResponse:
    """
    Redirect the currently logged-in user to their own profile page.
    """
    return redirect('users:profile', username=request.user.username)


@login_required
def profile_edit_view(request: HttpRequest, username: str) -> HttpResponse:
    """
    View for editing the user's own profile.
    """
    User = get_user_model()
    user = get_object_or_404(User, username=username)

    if request.user != user:
        return HttpResponseForbidden(
            "You are not allowed to edit this profile."
        )

    if request.method == 'POST':
        form = ProfileUpdateForm(request.POST, request.FILES, instance=user)
        if form.is_valid():
            form.save()
            messages.success(request, "Profile updated successfully!")
            return redirect('users:profile', username=user.username)
    else:
        form = ProfileUpdateForm(instance=user)

    return render(
        request, 'users/profile_edit.html', {'form': form, 'user': user}
    )
