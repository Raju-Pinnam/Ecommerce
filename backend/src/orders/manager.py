from django.db import models


class OrderManager(models.Manager):
    def new_or_get(self, billing_profile, cart_obj):
        qs = self.get_queryset().filter(billing_profile=billing_profile, cart=cart_obj, active=True, status='created')
        if qs.count() == 1:
            obj = qs.first()
            order_obj_created = False
        else:
            obj = self.model.objects.create(billing_profile=billing_profile, cart=cart_obj)
            order_obj_created = True
        return obj, order_obj_created
