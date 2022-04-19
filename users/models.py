from typing import Counter
from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser


class UserManager(BaseUserManager):
    def create_user(self, phone, name):
        """
        Creates and saves a User with the given phone and name.
        """

        if not phone:
            raise ValueError('Users must have a phone number')

        user = self.model(
            phone=phone,
            name=name,
        )

        user.set_password(None)
        user.save(using=self._db)
        return user

    def create_superuser(self, phone, name, password):
        """
        Creates and saves a superuser with the given phone, name and password.
        """
        user = self.create_user(
            phone,
            name,
        )
        user.set_password(password)
        user.is_admin = True
        user.save(using=self._db)
        return user


# Create your models here.
class User(AbstractBaseUser):
    phone = models.CharField(max_length=13, unique=True)
    name = models.CharField(max_length=50)
    counter = models.IntegerField(default=0, blank=True)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = UserManager()

    USERNAME_FIELD = 'phone'
    REQUIRED_FIELDS = ['name']

    def __str__(self):
        return self.name

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return self.is_admin

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True

    @property
    def is_staff(self):
        "Is the user a member of staff?"
        # Simplest possible answer: All admins are staff
        return self.is_admin