from django.contrib import admin
from .models import *
# Register your models here.
@admin.register(Task)
class StudentAdmin(admin.ModelAdmin):
    list_display=['id','name','roll','city']

# @admin.register(Class)
# class ClassAdmin(admin.ModelAdmin):
#     list_display=['id','class_name','section']


