from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import pre_save, m2m_changed

from products.models import Product

from .managers import CartManager


class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    products = models.ManyToManyField(Product, blank=True)
    subtotal = models.DecimalField(default=0.00, decimal_places=2, max_digits=15)
    total = models.DecimalField(default=0.00, decimal_places=2, max_digits=15)
    cart_created_time = models.DateTimeField(auto_now_add=True)
    cart_updated_time = models.DateTimeField(auto_now=True)

    objects = CartManager()

    def __str__(self):
        return str(self.id)


def m2m_changed_cart_receiver(sender, instance, action, *args, **kwargs):
    if action == 'post_add' or action == 'post_remove' or action == 'post_clear':
        products = instance.products.all()
        total = 0
        for x in products:
            total += x.price
        instance.subtotal = total
        instance.save()


m2m_changed.connect(m2m_changed_cart_receiver, sender=Cart.products.through)


def pre_save_receiver_signal(sender, instance, *args, **kwargs):
    if instance.subtotal <= 0:
        instance.total = 0
    else:
        delivery_charges = 45           # TODO shipping charges and discounts may have to enter
        instance.total = instance.subtotal + delivery_charges


pre_save.connect(pre_save_receiver_signal, sender=Cart)
