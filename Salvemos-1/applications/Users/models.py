from django.db import models
from django.conf import settings
from django.contrib.auth.models import (
    AbstractBaseUser,
    PermissionsMixin,
)
from model_utils.models import TimeStampedModel
#
from .managers import UserManager, FavoritesManager
from applications.Posts.models import Posts
# Create your models here.


class User(AbstractBaseUser, PermissionsMixin):
    """Modelo para la creación de un usuario"""
    GENDER_CHOICES = (
        ('M', 'Masculino'),
        ('F', 'Femenino'),
        ('O', 'Otros'),
    )

    email = models.EmailField(unique=True)
    name = models.CharField('Nombres', max_length=30)
    last_name = models.CharField('Apellidos', max_length=40, blank=True)
    is_foundation = models.BooleanField(default=False)

    genero = models.CharField(
        max_length=1,
        choices=GENDER_CHOICES,
        blank=True
    )
    date_birth = models.DateField(
        'Fecha de nacimiento',
        blank=True,
        null=True
    )
    #
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)
    codregistro = models.CharField(max_length=6, default='000000')

    USERNAME_FIELD = 'email'

    REQUIRED_FIELDS = ['name']

    objects = UserManager()

    def get_short_name(self):
        return self.name

    def get_full_name(self):
        return self.name + ' ' + self.last_name


class Favorites(TimeStampedModel):
    """Modelo para los favoritos de un usuario"""
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name='user_favorites',
        on_delete=models.CASCADE,
    )
    post = models.ForeignKey(
        Posts,
        related_name='posts_favorites',
        on_delete=models.CASCADE,
    )
    objects = FavoritesManager()

    class Meta:
        unique_together = ('user', 'post')
        verbose_name = 'Post Favorito'
        verbose_name_plural = 'Posts Favoritos'

    def __str__(self):
        return self.post.title
