from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from .forms import CustomUserCreationForm, UserForm,Product_Add_Form
from django.contrib.auth.forms import AuthenticationForm
from .models import *

def login_view(request):
    if request.method == 'POST':
        form = UserForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('home')  # Redirect to the home page after successful login
        else:
            # Invalid credentials
            return render(request, 'login.html', {'form': form, 'error': 'Invalid username or password'})
    else:
        form =UserForm()

    return render(request, 'login.html', {'form': form})


def register_view(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login_view')  # Redirect to the login page after successful registration
    else:
        form = CustomUserCreationForm()
    
    return render(request, 'register.html', {'form': form})


def home(request):
    return render(request, 'home.html')


def Add_Product(request):
    if request.method == 'POST':
        form = Product_Add_Form(request.POST, request.FILES)
        print("hello")
        if form.is_valid():
            print("hello2")
            form.save()
            user=Product.objects.all()
            return render(request,'home.html',{'user':user})  # Redirect to the home page or any other page
    else:
        form = Product_Add_Form()

    return render(request, 'add.html', {'form': form})

