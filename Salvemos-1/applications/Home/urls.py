"""Urls de la aplicación Home"""
from django.urls import path

from . import views

app_name = "Home_app"

urlpatterns = [
    path(
        '',
        views.HomePageView.as_view(),
        name='index',
    ),
    path(
        'contactanos/',
        views.ContactView.as_view(),
        name='contactanos',
    ),
]
