from django import forms
from django.contrib.auth.models import User

from post.models import Transactions


class AddTransactionForm(forms.ModelForm):
    class Meta:
        model = Transactions
        fields = ('amount',)
