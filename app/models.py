import datetime

from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.core.validators import RegexValidator
from django.db import models
from django.db.models import BooleanField


class CustomUserManager(BaseUserManager):
    def create_user(self, phonenumber, password, **extra_fields):

        if not phonenumber:
            raise ValueError("The phonenumber must be set")
        user = self.model(phonenumber=phonenumber, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, phonenumber, password, **extra_fields):

        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_admin", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")

        user = self.create_user(phonenumber, password, **extra_fields)

        user.is_admin = True
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser):
    is_admin = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_shop_owner = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    numeric = RegexValidator(r'09(1[0-9]|3[1-9]|2[1-9])-?[0-9]{3}-?[0-9]{4}',
                             'Only digit  and 11 characters with 0 at first of that.',
                             code='invalid_phonenumber')
    username = models.CharField(max_length=30)
    # password = models.CharField(max_length=100)
    choices = (('male', 'male'), ('female', 'female'))
    gender = models.CharField(max_length=10, choices=choices)
    birthdate = models.DateField(default=datetime.datetime.now)
    phonenumber = models.CharField(unique=True, validators=[numeric], max_length=11)

    USERNAME_FIELD = "phonenumber"
    objects = CustomUserManager()

    def __str__(self):
        return str(self.phonenumber)

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        return True

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True

    # @property
    # def is_staff(self):
    #     "Is the user a member of staff?"
    #     # Simplest possible answer: All admins are staff
    #     return self.is_admin

# Create your models here.
