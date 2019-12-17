import random

from AB_main.utils import random_string_generator

ORDER_STATUS_CHOICES = (
    ('created', 'Created'),
    ('paid', 'Paid'),
    ('shipped', 'Shipped'),
    ('refunded', 'Refunded'),
    ('canceled', 'Canceled'),
    ('completed', 'Completed'),
)


def unique_order_id_generator(instance):
    new_order_id = random_string_generator().upper()
    Klass = instance.__class__
    qs_exists = Klass.objects.filter(order_id=new_order_id).exists()
    if qs_exists:
        return unique_order_id_generator(instance)
    return new_order_id
