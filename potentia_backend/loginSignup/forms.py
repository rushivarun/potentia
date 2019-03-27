from django import forms
from django.contrib.auth.models import User

from loginSignup.models import AddSignup


class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())
    class Meta:
        model = User
        fields = ('username', 'password', 'email')

class AddSignupForm(forms.ModelForm):
    class Meta:
        model = AddSignup
        fields = ('address', 'phone', 'renewable_source')

