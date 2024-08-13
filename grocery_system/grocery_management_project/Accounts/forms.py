from django import forms
from .models import *


class UserForm(forms.ModelForm):
    # password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}), max_length=128)
    # confirm_password=forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}),max_length=128)
    class Meta:
        model =usermodel
        fields = ['username','email','password','confirm_password']   # Include other fields if needed
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control'}),
            'email':forms.TextInput(attrs={'class':'form-control'}),
            'password': forms.PasswordInput(attrs={'class': 'form-control'}),
            'confirm_password': forms.PasswordInput(attrs={'class': 'form-control'})
        }

