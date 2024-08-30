from django import forms
from .models import *
# from django.core import validators
from django.core.exceptions import ValidationError



def validate_start_with_s(value):
    print(value)
    if len(value)<5:
        raise forms.ValidationError('Name should start with s')
    
    
def mail_validate(value):
    if (value[-3] and value[-4]) != '.':
        raise forms.ValidationError("mail id not valid")

def pass_validate(value):
    if len(value)!= 8 and value!=value.uppercase():
        raise forms.ValidationError('password not correct')



class Userform(forms.ModelForm):
    # name=forms.CharField(validators=[validate_start_with_s]) 
    # email=forms.EmailField()
    # address=forms.CharField(widget=forms.Textarea()) 
    # contact=forms.IntegerField()
    # # password=forms.CharField()

    class Meta:
        model=Student
        fields = ['name', 'email', 'address', 'contact']
   
    # def clean_validation(self):
    #     name=self.cleaned_data.get('name')
    #     email=self.cleaned_data.get('email')
    #     if name[0]!='s':
    #         raise ValidationError('name is not satisfied')
        
    #     if email[-3]!='.' and email[-4]!='.':
    #         raise ValidationError('mail is not correct') 
        
        
    # def clean_name(self):
    #     name = self.cleaned_data.get('name')
    #     validate_start_with_s(name)
    #     return name
    # def clean(self):
    #     cleaned_data = super().clean()
    #     name = cleaned_data.get('name')
    #     # Example validation: name must not contain digits
    #     if len(name)<5:
    #         self.add_error('name', 'Name should not contain digits.')
    #     # Example validation: age must be positive
    #     return cleaned_data
        
    
    
      
      
       
   
   