import datetime

from django.contrib.auth.models import User
from django.db import models


class Usermodel(models.Model):
    # username = models.CharField(max_length=10, choices=tuple(choices))
    username = models.OneToOneField(User, on_delete=models.CASCADE)
    password = models.CharField(max_length=100)
    choices = (('male', 'male'), ('female', 'female'))
    # username = models.CharField(max_length=50)
    gender = models.CharField(max_length=10, choices=choices)
    birthdate = models.DateField(default=datetime.datetime.now())
    phonenumber = models.IntegerField(unique=True)

    # password = models.CharField(max_length=50)

    def __str__(self):
        return str(self.phonenumber)

# Create your models here.
