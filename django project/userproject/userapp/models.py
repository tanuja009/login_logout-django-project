from django.db import models
from django.contrib.auth.hashers import make_password

# Create your models here.

class usermodel(models.Model):
    name=models.CharField(max_length=100)
    email=models.EmailField(unique=True)
    password=models.CharField(max_length=128)
    
    

    def set_password(self, raw_password):
        self.password = make_password(raw_password)

    