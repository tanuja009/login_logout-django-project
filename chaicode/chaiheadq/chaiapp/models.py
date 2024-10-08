from django.db import models
from django.contrib.auth.models import User 
# Create your models here.

class Tweet(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    text=models.TextField()
    photo=models.ImageField(blank=True,null=True,upload_to='photos/')
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.user.username}-{self.text[:10]}'
    
class Category(models.Model):
    category_name=models.CharField(max_length=50)

    def __str__(self):
        return self.category_name


