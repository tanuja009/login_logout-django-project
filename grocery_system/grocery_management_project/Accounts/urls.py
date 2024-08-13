from django.contrib import admin
from django.urls import path
from Accounts import views

urlpatterns = [
   path('',views.user_login,name='login'),
   path('logout/',views.user_logout,name="logout"),
   path('home/',views.home,name='home')
]