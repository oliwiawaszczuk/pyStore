from django import forms
from django.contrib.auth import authenticate, login
from .models import User

class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password']