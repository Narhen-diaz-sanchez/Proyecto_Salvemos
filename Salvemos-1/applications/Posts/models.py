"""Modelos de la aplicación entradas"""
from datetime import timedelta, datetime
from django.db import models
from django.conf import settings
from django.template.defaultfilters import slugify
from django.urls import reverse_lazy
from django.db.models.deletion import CASCADE
# App terceros
from model_utils.models import TimeStampedModel
from ckeditor_uploader.fields import RichTextUploadingField
# Managers
from .managers import PostsManager


class Category(TimeStampedModel):
    """Categorias de una entrada"""
    name = models.CharField('Nombre', max_length=30, unique=True)

    class Meta:
        verbose_name = 'Categoria'
        verbose_name_plural = 'Categorias'

    def __str__(self):
        return str(self.id) + '. ' + self.name


class Tag(TimeStampedModel):
    """Etiquetas de un articulo"""
    name = models.CharField('Nombre', max_length=30)

    class Meta:
        verbose_name = 'Etiqueta'
        verbose_name_plural = 'Tags'

    def __str__(self):
        return self.name


class Posts(TimeStampedModel):
    """Modelo para los Posts"""

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
    )
    tag = models.ManyToManyField(Tag)
    title = models.CharField(
        'Titulo',
        max_length=200
    )
    resume = models.TextField('Resumen')
    content = RichTextUploadingField('Contenido')
    public = models.BooleanField(default=False)
    image = models.ImageField(
        'Imagen',
        upload_to='Posts'
    )
    slug = models.SlugField(editable=False, max_length=300)

    objects = PostsManager()

    class Meta:
        verbose_name = "Post"
        verbose_name_plural = 'Posts'

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse_lazy(
            'Posts_app:Posts-detail',
            kwargs={'slug': self.slug})

    def save(self, *args, **kwargs):
        # Se reescribe la funcion save para modificar el slug y que quede como unico para usarlo en las urls
        # Calculamos el total de segundos de la hora actual
        now = datetime.now()
        total_time = timedelta(
            hours=now.hour,
            minutes=now.minute,
            seconds=now.second,
        )
        seconds = int(total_time.total_seconds())
        slug_unique = '%s %s' % (self.title, str(seconds))

        self.slug = slugify(slug_unique)
        super(Posts, self).save(*args, **kwargs)
