"""Urls de la aplicación Posts"""
from django.urls import path
from . import views

app_name = "Posts_app"

urlpatterns = [
    path(
        'Posts/',
        views.PostsListView.as_view(),
        name='Posts-lista',
    ),
    path(
        'Post/<slug>/',
        views.PostsDetailView.as_view(),
        name='Post-detail',
    ),
    path(
        'NewPost/',
        views.NewPost.as_view(),
        name='NewPost',
    ),
]
