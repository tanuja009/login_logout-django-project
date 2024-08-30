from django import forms
from django.contrib.auth.models import User
class userform(forms.ModelForm):
    class Meta:
        model=User
        fields=['email','password']

        widget={
            'email': forms.TextInput(attrs={'class': 'form-control'}),
            'password': forms.PasswordInput(attrs={'class': 'form-control'}),
        }
