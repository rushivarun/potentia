from django.contrib.auth.models import User
from django.db import models

# Create your models here.


class Transactions(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user")
    tosenduser = models.ForeignKey(User, on_delete=models.CASCADE, related_name="tosenduser")
    amount = models.IntegerField()
    cost = models.IntegerField()