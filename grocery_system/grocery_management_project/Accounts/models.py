from django.db import models

from django.core.exceptions import ValidationError
# from django.contrib.auth.models import AbstractUser

# # Create your models here.


# class CustomUser(AbstractUser):
#     username=None
#     phone_no=models.IntegerField(unique=True)
#     user_bio=models.CharField(max_length=100)
#     password = models.CharField( max_length=128)
#     email=models.EmailField(max_length=100)
#     confirm_password=models.CharField(max_length=128)

    
#     USERNAME_FIELD=['phone_no','user_bio','password','email','confirm_password']
#     REQUIRED_FIELDS=[]

class usermodel(models.Model):
    username=models.CharField(max_length=100)
    phone_no=models.IntegerField(unique=True)
    email=models.EmailField(max_length=100)
    password = models.CharField( max_length=128)
    confirm_password=models.CharField(max_length=128)

    def clean_password(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")

        if password and confirm_password and password != confirm_password:
            raise ValidationError("Passwords do not match")

        return cleaned_data

    
