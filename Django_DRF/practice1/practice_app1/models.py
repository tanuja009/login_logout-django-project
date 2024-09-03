from django.db import models

# Create your models here.

class Task(models.Model):
    name=models.CharField(max_length=100)
    roll=models.IntegerField()
    city=models.CharField(max_length=100)

    def __str__(self):
        return self.name
    
# class Class(models.Model):
#     class_name=models.CharField(max_length=50)
#     section=models.CharField(max_length=50)
#     url=models.URLField(blank=True,null=True)

