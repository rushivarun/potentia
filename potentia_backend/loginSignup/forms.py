from django import forms
from django.contrib.auth.models import User
from .models import addSignup



class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())
    class Meta():
        model = User
        fields = ('username', 'password', 'email')

class addSignupForm(forms.ModelForm):
    class Meta():
        model = addSignup
        fields = ('address', 'phone', 'renewable_source')
