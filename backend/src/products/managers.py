from django.db import models
from django.db.models import Q


class ProductQueryset(models.query.QuerySet):
    def is_coming(self):
        return self.filter(is_coming=True)

    def search(self, query):
        lookups = (Q(name__icontains=query) |
                   Q(slug__icontains=query) |
                   Q(description__icontains=query))
        return self.filter(lookups).distinct()


class ProductManager(models.Manager):
    def get_queryset(self):
        return ProductQueryset(self.model, using=self._db)

    def is_coming(self):
        return self.get_queryset().is_coming()

    def get_by_id(self, product_id):
        qs = self.get_queryset().filter(id=product_id)
        product_obj = None
        is_exists = False
        if qs.count() == 1:
            product_obj = qs.first()
            is_exists = True
        print('id :', product_id, 'product_obj : ', product_obj, 'is_exists: ', is_exists)
        return product_obj, is_exists

    def search(self, query):

        return self.get_queryset().search(query)
