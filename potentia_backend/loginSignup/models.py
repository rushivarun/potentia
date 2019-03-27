from django.contrib.auth.models import AbstractUser
from django.db import models
from django.contrib.auth.models import User
from django.contrib.postgres.fields import ArrayField

# Create your models here.

class addSignup(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)


    address = models.CharField(max_length = 100)
    phone = models.IntegerField()
    renewable_source = models.CharField(max_length = 100)
