from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('students_deatils/', views.students_deatils.as_view(), name="task"), 
]