from django import forms
from .models import Student
from django.core.exceptions import ValidationError

class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = Student
        fields = ['name','contact','email','password']

    
    def clean_email(self):
        email = self.cleaned_data.get('email')
        if not email.endswith('.com'):
            raise ValidationError("The email must end with '.com'")
        return email
    def clean_contact(self):
        contact=self.cleaned_data('contact')
        if len(contact)!=10:
            raise ValidationError('contact always have 10 digits')
        return contact


    def clean_password(self):
        password = self.cleaned_data.get('password')
    
    # Check if the password is at least 8 characters long
        if len(password) < 8:
            raise ValidationError("The password must be at least 8 characters long.")
    
    # Check if the password contains at least one special character
        special_characters = {'@', '#', '%', '&', '*'}
        if not any(char in special_characters for char in password):
            raise ValidationError("The password must contain at least one special character (@, #, %, &, *).")
        return password


class loginform(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    class Meta:
        model=Student
        fields=['email','password']




    def clean_email(self):
        email = self.cleaned_data.get('email')
        if not email.endswith('.com'):
            raise ValidationError("The email must end with '.com'")
        return email



    def clean_password(self):
        password = self.cleaned_data.get('password')
    
    # Check if the password is at least 8 characters long
        if len(password) < 8:
            raise ValidationError("The password must be at least 8 characters long.")
    
    # Check if the password contains at least one special character
        special_characters = {'@', '#', '%', '&', '*'}
        if not any(char in special_characters for char in password):
            raise ValidationError("The password must contain at least one special character (@, #, %, &, *).")
        return password




