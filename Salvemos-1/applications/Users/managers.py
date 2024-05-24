from django.db import models
#
from django.contrib.auth.models import BaseUserManager


class UserManager(BaseUserManager, models.Manager):

    def _create_user(self, email, password, is_staff, is_superuser, is_active, **extra_fields):
        user = self.model(
            email=email,
            is_staff=is_staff,
            is_superuser=is_superuser,
            is_active=is_active,
            **extra_fields
        )
        user.set_password(password)
        user.save(using=self.db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        """Crea los ususario de la página"""
        return self._create_user(email, password, False, False, False, **extra_fields)

    def create_superuser(self, email, password=None, **extra_fields):
        """Crea los superusuarios"""
        return self._create_user(email, password, True, True, True, **extra_fields)

    def cod_validation(self, id_user, cod_registro):
        """Metodo para validar el código de confirmación del correo"""
        if self.filter(id=id_user, codregistro=cod_registro).exists():
            return True
        else:
            return False


class FavoritesManager(models.Manager):
    """Función que devuelve los favoritos de un usuario"""

    def posts_user(self, usuario):
        return self.filter(
            post__public=True,
            user=usuario
        ).order_by('-created')
