from django.db import models
from model_utils.models import TimeStampedModel

# Create your models here.


class Contact(TimeStampedModel):
    """Modelo para formulario de contacto"""
    full_name = models.CharField('Nombres', max_length=60)
    email = models.EmailField()
    message = models.TextField()

    class Meta:
        verbose_name = 'Contacto'
        verbose_name_plural = 'Mensaje'

    def __str__(self):
        return self.full_name
