from django.db import models


# Create your models here.
class GuestUser(models.Model):
    email = models.EmailField(max_length=250)
    active = models.BooleanField(default=True)
    updated = models.DateTimeField(auto_now=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.email
