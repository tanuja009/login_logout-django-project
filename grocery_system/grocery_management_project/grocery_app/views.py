from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login,logout
from django.contrib.auth.decorators import login_required
from .forms import CustomUserCreationForm, UserForm,Product_Add_Form
from django.core.exceptions import ValidationError
from django.contrib.auth.forms import AuthenticationForm
from .models import *
from django.contrib.auth.models import User

def login_view(request):
    if request.method == 'POST':
        form = UserForm(request.POST)
        if form.is_valid():
            # Extract email and password from form
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            
            # Authenticate user
            user = authenticate(request, username=email, password=password)
            
            if user is not None:
                # Log in user
                login(request, user)
                return redirect('home')  # Redirect to the home page after successful login
            else:
                # Invalid credentials
                return render(request, 'login.html', {'form': form, 'error': 'Invalid email or password'})
    else:
        form = UserForm()
    
    return render(request, 'login.html', {'form': form})


def register_view(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            
            name=form.cleaned_data['username']
            email=form.cleaned_data['email']
            fname=form.cleaned_data['first_name']
            lname=form.cleaned_data['last_name']
            pass1=form.cleaned_data['password1']
            pass2=form.cleaned_data['password2']
            
            if User.objects.filter(email=email).exists():
                raise ValidationError("A user with this email already exists.")# Use ValidationError or similar
            User.objects.create(username=name,email=email,first_name=fname,last_name=lname,password1=pass1,password2=pass2)
            data.objects.create(username=name,email=email,first_name=fname,last_name=lname,password1=pass1,password2=pass2)

            return redirect('login_view')  # Redirect to the login view # Redirect to the login page after successful registration
    else:
        form = CustomUserCreationForm()
    
    return render(request, 'register.html', {'form': form})


def home(request):
  info=Product.objects.all()
  carousal_image=Product.objects.values_list('carousal_image', flat=True)
  return render(request,"home.html",{'user':info})


def Add_Product(request):
    if request.method == 'POST':
        form = Product_Add_Form(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            user=Product.objects.all()
            return render(request,'home.html',{'user':user})  # Redirect to the home page or any other page
    else:
        form = Product_Add_Form()

    return render(request, 'add.html', {'form':form})


def About(request):
    return render(request,"About.html")

@login_required(login_url='login_view')
def logout_view(request):
    logout(request)
    return redirect('login_view')

