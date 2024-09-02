from django import forms
from .models import Tweet
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.forms import AuthenticationForm

class TweetForm(forms.ModelForm):
    class Meta:
        model = Tweet
        fields = ['text', 'photo']

class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']
        error_messages = {
            'username': {
                'required': 'Please enter a username.',
                'max_length': 'Username is too long.',
            },
            'email': {
                'required': 'Please enter your email address.',
                'invalid': 'Enter a valid email address.',
            },
            'password1': {
                'required': 'Please enter a password.',
                'password_mismatch': 'The two password fields must match.',
            },
            'password2': {
                'required': 'Please confirm your password.',
                'password_mismatch': 'The two password fields must match.',
            },
        }

class CustomAuthenticationForm(AuthenticationForm):
    class Meta:
        model=User
        fields=['username','email','password']
        error_messages = {
            'username': {
                'required': 'Please enter a username.',
                'max_length': 'Username is too long.',
            },
            'email': {
                'required': 'Please enter your email address.',
                'invalid': 'Enter a valid email address.',
            },
            'password1': {
                'required': 'Please enter a password.',
                'password_mismatch': 'The two password fields must match.',
            },
        }
