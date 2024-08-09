from django.contrib import admin
from .models import *
# Register your models here.
admin.site.register(Category)
admin.site.register(Product)
admin.site.register(QuantityVarienty)
admin.site.register(SizeVarient)
admin.site.register(ColorVarient)
admin.site.register(ProductImages)