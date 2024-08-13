from django.shortcuts import render,redirect
from .forms import *
from django.http import HttpResponse
# Create your views here.
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User

from django.contrib.auth.decorators import login_required

def user_login(request):
    if request.method == 'POST':
        form = UserForm(request.POST)
        if form.is_valid():
            name=form.cleaned_data['username']
            pass_user=form.cleaned_data['password']
            user=authenticate(request,username=name,password=pass_user)
            login(request, user)
            return redirect('home')#Redirect to home page or any other page
        else:
            return render(request,"login.html",{'error':"user not found"})
    else:
        form = UserForm()
    return render(request, 'login.html', {'form': form})

def user_logout(request):
    logout(request)
    return redirect('login')  # Redirect to login page after logout

@login_required
def home(request):
    return render(request, 'home.html')


