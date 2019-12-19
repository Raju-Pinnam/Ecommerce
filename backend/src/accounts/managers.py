from django.contrib.auth.models import BaseUserManager


class UserManager(BaseUserManager):
    def create_user(self, email, name, password=None, is_staff=False, is_admin=False, is_active=True):
        if not email:
            raise ValueError("you must provide email address")
        if not password:
            raise ValueError("User must provide password")
        user = self.model(
            email=self.normalize_email(email)
        )
        user.name = name
        user.is_staff = is_staff
        user.is_admin = is_admin
        user.is_active = is_active
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_staffuser(self, email, name, password=None):
        user = self.create_user(email=email, name=name, password=password, is_staff=True, is_admin=False,
                                is_active=True)
        return user

    def create_superuser(self, email, name, password=None):
        user = self.create_user(email=email, name=name, password=password, is_staff=True, is_admin=True,
                                is_active=True)
        return user

