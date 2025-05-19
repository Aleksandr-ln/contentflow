from django.urls import path

from . import views

urlpatterns = [
    path(
        '',
        views.post_list_view,
        name='post-list'),
    path(
        'create/',
        views.post_create_view,
        name='post-create'),
    path(
        'tag/<str:tag_name>/',
        views.post_list_by_tag,
        name='post-by-tag'),
    path(
        'post/<int:pk>/edit/',
        views.PostUpdateView.as_view(),
        name='post-edit'),
    path(
        '<int:pk>/delete/',
        views.PostDeleteView.as_view(),
        name='post-delete'),
]
