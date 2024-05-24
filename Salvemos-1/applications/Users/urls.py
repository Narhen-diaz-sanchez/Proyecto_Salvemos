"""URls de la aplicación Users"""
from django.urls import path

from . import views

app_name = "Users_app"

urlpatterns = [
    path(
        'register/',
        views.UserRegisterView.as_view(),
        name='user-register',
    ),
    path(
        'verification/<pk>/',
        views.CodVerificationView.as_view(),
        name='user-verification',
    ),
    path(
        'login/',
        views.LoginUser.as_view(),
        name='user-login',
    ),
    path(
        'logout/',
        views.LogoutView.as_view(),
        name='user-logout',
    ),
    path(
        'update/',
        views.UpdatePasswordView.as_view(),
        name='user-update',
    ),
    path(
        'profile/',
        views.UserPageListView.as_view(),
        name='user-profile',
    ),
    path(
        'addfavorito/<pk>/',
        views.addfavoritosView.as_view(),
        name='addfavorito',
    ),
    path(
        'deletefavorito/<pk>/',
        views.FavoritosDeleteView.as_view(),
        name='deletefavorito',
    ),
]
