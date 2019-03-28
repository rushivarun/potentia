from django.contrib.auth.models import AbstractUser
from django.db import models
from django.contrib.auth.models import User
from django.contrib.postgres.fields import ArrayField

# Create your models here.
from django.db.models.signals import post_save
from django.dispatch import receiver



class AddSignup(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='additional')
    address = models.CharField(max_length = 100)
    phone = models.IntegerField()
    renewable_source = models.CharField(max_length = 100)
    Potentia = models.IntegerField(default=0)
    flares = models.IntegerField(default=0)

#
# @receiver(post_save, sender=User)
# def create_user_profile(sender, instance, created, **kwargs):
#     if created:
#         AddSignup.objects.create(user=instance)
#
# @receiver(post_save, sender=User)
# def save_user_profile(sender, instance, **kwargs):
#     instance.profile.save()