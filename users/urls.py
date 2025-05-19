from django.urls import path

from . import views
from .views import activate_user, profile_edit_view, profile_view

app_name = 'users'

urlpatterns = [
    path('register/', views.register_view, name='register'),
    path('activate/<uidb64>/<token>/', activate_user, name='activate'),
    path('profile/', views.redirect_to_own_profile, name='my-profile'),
    path('<str:username>/edit/', profile_edit_view, name='profile-edit'),
    path('<str:username>/', profile_view, name='profile'),
]
