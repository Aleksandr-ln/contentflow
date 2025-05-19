from django.urls import path

from .views import like_toggle_ajax

urlpatterns = [
    path('ajax/like-toggle/', like_toggle_ajax, name='like-toggle-ajax'),
]
