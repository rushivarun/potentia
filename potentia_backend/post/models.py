from django.contrib.auth.models import User
from django.db import models

# Create your models here.


class Transactions(models.Model):
    trans_id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user")
    tosenduser = models.ForeignKey(User, on_delete=models.CASCADE, related_name="tosenduser", null=True)
    amount = models.IntegerField()
    cost = models.IntegerField()
    sent_transfer_tx = models.TextField(null=True)
    sent_creation_tx = models.TextField(null=True)
    status = models.BooleanField(default=False)