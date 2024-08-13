from django.db import models

# Create your models here.
class data(models.Model):
    username=models.CharField(max_length=100)
    email=models.EmailField()
    password=models.CharField(max_length=100)
    confirm_password=models.CharField(max_length=100)

    def __str__(self):
        return self.username



class Product(models.Model):
    product_name = models.CharField(max_length=100)
    image = models.ImageField(upload_to='product/')
    description = models.TextField()
    price = models.FloatField()

    def __str__(self):
        return self.product_name


