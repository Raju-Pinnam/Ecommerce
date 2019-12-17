from django.db import models
from django.db.models.signals import pre_save
from django.shortcuts import redirect
from django.urls import reverse

from .utils import upload_file_path, unique_slug_generator
from .managers import ProductManager


class Product(models.Model):
    name = models.CharField(max_length=255)
    slug = models.SlugField(blank=True, null=True, unique=True)
    description = models.TextField()
    price = models.DecimalField(decimal_places=2, max_digits=10, default=0.00)
    product_front_image = models.ImageField(upload_to=upload_file_path, null=True, blank=True)
    is_coming = models.BooleanField(default=False)

    objects = ProductManager()

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('products:product_slug', kwargs={'slug': self.slug})


def product_pre_save_receiver(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = unique_slug_generator(instance)


pre_save.connect(product_pre_save_receiver, sender=Product)
