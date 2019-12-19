from django.conf import settings
from django.db import models
from django.db.models.signals import post_save

from billing.managers import BillingProfileManager

User = settings.AUTH_USER_MODEL


class BillingProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, blank=True, null=True)
    email = models.EmailField(max_length=255)
    active = models.BooleanField(default=True)
    update = models.DateTimeField(auto_now=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    objects = BillingProfileManager()

    def __str__(self):
        return self.email


# def billing_profile_receiver(sender, instance, created, *args, **kwargs):
#     if created:
#         print('send to installed payment gateways')
#         instance.customer_id = new_id
#         instance.save()

def user_saved_receiver(sender, instance, created, *args, **kwargs):
    if created and instance.email:
        BillingProfile.objects.get_or_create(user=instance, email=instance.email)


post_save.connect(user_saved_receiver, sender=User)
