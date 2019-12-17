from django.db import models

from accounts.models import GuestUser


class BillingProfileManager(models.Manager):
    def new_or_get(self, request):
        guest_email_id = request.session.get('guest_email_id')
        obj = None
        is_created = False
        if request.user.is_authenticated:
            if request.user.email:
                obj, is_created = self.model.objects.get_or_create(user=request.user,
                                                                   email=request.user.email)
        elif guest_email_id is not None:
            guest_email_obj = GuestUser.objects.get(id=guest_email_id)
            obj, is_created = self.model.objects.get_or_create(
                email=guest_email_obj.email)
        else:
            pass
        return obj, is_created
