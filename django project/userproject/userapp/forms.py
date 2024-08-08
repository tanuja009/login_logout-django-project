from django import forms
from .models import usermodel

class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
   

    class Meta:
        model=usermodel
        fields=['name','email','password']

    
    