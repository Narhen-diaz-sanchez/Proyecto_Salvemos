from django.db import models


class PostsManager(models.Manager):
    """Procedimiento para Post"""

    def Post_en_portada_adopcion(self):
        """Devuelve los ultimos tres posts de categoria adopción"""
        return self.filter(
            public=True,
            category='1',
        ).order_by('-created')[:3]

    def Post_en_portada_apadrinar(self):
        """Devuelve los ultimos tres posts de categoria apadrinar"""
        return self.filter(
            public=True,
            category='2',
        ).order_by('-created')[:3]

    def Post_en_portada_donar(self):
        """Devuelve los ultimos tres posts de categoria donar"""
        return self.filter(
            public=True,
            category='3',
        ).order_by('-created')[:3]

    def buscar_Post(self, kword, categoria):
        """Procedimiento para buscar Posts por palabra clave o categoría"""
        if len(categoria) > 0:
            return self.filter(
                category__name=categoria,
                title__icontains=kword,
                public=True,
            ).order_by('-created')
        else:
            return self.filter(
                title__icontains=kword,
                public=True,
            ).order_by('-created')
