from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('student/',views.StudentList.as_view()),
    
]