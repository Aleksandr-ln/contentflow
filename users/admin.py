from django.contrib import admin
from django.utils.html import format_html

from .models import User


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = (
        'avatar_preview',
        'email',
        'full_name',
        'is_active',
        'is_staff')
    search_fields = ('email', 'full_name')
    list_filter = ('is_active', 'is_staff', 'is_superuser')
    readonly_fields = ('last_login', 'date_joined')

    def avatar_preview(self, obj):
        if obj.avatar:
            return format_html(
                '<img src="{}" width="40" style="border-radius:50%;">',
                obj.avatar.url)
        return "-"
    avatar_preview.short_description = "Avatar"
