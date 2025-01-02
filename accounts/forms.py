from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticatingForm
from .models import CustomUser

class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'phone', 'address', 'password1', 'password2']

class CustomAuthenticatioForm(AuthenticatingForm):
    class Meta:
        model = CustomUser
        fields = ['username', 'password']