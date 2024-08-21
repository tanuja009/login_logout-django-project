from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.contrib.auth import authenticate, login,logout
from django.contrib.auth.decorators import login_required
from .forms import Product_Add_Form
from django.core.exceptions import ValidationError
from django.contrib.auth.forms import AuthenticationForm
from .models import *
from django.contrib.auth.models import User

# def login_view(request):
#     if request.method == 'POST':
#         form = UserForm(request.POST)
#         if form.is_valid():
#             # Extract email and password from form
#             email = form.cleaned_data['email']
#             password = form.cleaned_data['password']
            
#             # Authenticate user
#             user = authenticate(request, username=email, password=password)
            
#             if user is not None:
#                 # Log in user
#                 login(request, user)
#                 return redirect('home')  # Redirect to the home page after successful login
#             else:
#                 # Invalid credentials
#                 return render(request, 'login.html', {'form': form, 'error': 'Invalid email or password'})
#     else:
#         form = UserForm()
    
#     return render(request, 'login.html', {'form': form})



def SignupPage(request):
    if request.method=='POST':
        uname=request.POST.get('username')
        email=request.POST.get('email')
        pass1=request.POST.get('password1')
        pass2=request.POST.get('password2')

        if pass1!=pass2:
            return HttpResponse("Your password and confrom password are not Same!!")
        else:

            my_user=User.objects.create_user(uname,email,pass1)
            my_user.save()
            return redirect('login')
        



    return render (request,'signup.html')


# def register_view(request):
#     if request.method == 'POST':
#         form = CustomUserCreationForm(request.POST)
#         if form.is_valid():
            
#             name=form.cleaned_data['username']
#             email=form.cleaned_data['email']
#             fname=form.cleaned_data['first_name']
#             lname=form.cleaned_data['last_name']
#             pass1=form.cleaned_data['password1']
            
            
#             if User.objects.filter(email=email).exists():
#                 raise ValidationError("A user with this email already exists.")# Use ValidationError or similar
#             User.objects.create(username=name,email=email,first_name=fname,last_name=lname,password1=pass1)
#             data.objects.create(username=name,email=email,first_name=fname,last_name=lname,password1=pass1)

#             return redirect('login_view')  # Redirect to the login view # Redirect to the login page after successful registration
#     else:
#         form = CustomUserCreationForm()
    
#     return render(request, 'register.html', {'form': form})

def LoginPage(request):
    if request.method=='POST':
        username=request.POST.get('username')
        pass1=request.POST.get('pass')
        user=authenticate(request,username=username,password=pass1)
        if user is not None:
            login(request,user)
            return redirect('home')
        else:
            # messages.ERROR(request,"user name password are wrong")
            return redirect('login')
        

    return render (request,'login.html')


def home(request):
  products =Product.objects.all()
  data=category.objects.all()
 

  carousal_image=Product.objects.values_list('carousal_image', flat=True)
  return render(request,"home.html",{'products':products,'categories':data})


def About(request):
    return render(request,"about_us.html")

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


# def About(request):
#     return render(request,"about_us.html")

@login_required(login_url='login_view')
def logout_view(request):
    logout(request)
    return redirect('login_view')

def read_cat(request,id):
    category1=category.objects.get(id=id)
    product=get_object_or_404(Product,category=category1)
    cate=category.objects.all()
    return render(request,"fruits.html",{'data':product,'cate':cate})

def product_details(request, id):
    item = get_object_or_404(Product, id=id)
    return render(request, "details.html", {'item': item}) 


def card_read(request,id):
    item=Product.objects.filter(id=id)
    user=User.objects.all()






