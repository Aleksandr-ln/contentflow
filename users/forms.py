from typing import Any

from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password

User = get_user_model()


class UserRegisterForm(forms.ModelForm):
    """
    Registration form with username, email and password.
    """
    password = forms.CharField(widget=forms.PasswordInput)
    password_confirm = forms.CharField(
        label="Confirm password", widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['username', 'email', 'password']

    def clean_username(self) -> str:
        """
        Ensure that the username is unique.
        Raises ValidationError if the username already exists.
        """
        username = self.cleaned_data['username']
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError("This username is already taken.")
        return username

    def clean(self) -> dict[str, Any]:
        """
        Cross-field validation:
        - Checks that password and password_confirm match
        - Validates password strength using Django's built-in validators
        """
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        password_confirm = cleaned_data.get("password_confirm")

        if password and password_confirm and password != password_confirm:
            self.add_error("password_confirm", "Passwords do not match.")

        if password:
            try:
                validate_password(password)
            except forms.ValidationError as e:
                self.add_error("password", e)

        return cleaned_data


class ProfileUpdateForm(forms.ModelForm):
    """
    Form for updating user's profile information:
    full name, bio, and avatar.
    """
    class Meta:
        model = User
        fields = ['full_name', 'bio', 'avatar']
