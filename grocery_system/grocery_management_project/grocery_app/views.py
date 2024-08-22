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
  images = [
        "https://cdn.pixabay.com/photo/2022/08/01/07/59/vegetables-7357585_640.png",
        "https://5.imimg.com/data5/MG/FQ/SA/SELLER-283756/all-fmcg-grocery-products.jpg",
        "https://media.istockphoto.com/id/171302954/photo/groceries.jpg?s=612x612&w=0&k=20&c=D3MmhT5DafwimcYyxCYXqXMxr1W25wZnyUf4PF1RYw8="
    ]
 

#   carousal_image=Product.objects.values_list('carousal_image', flat=True)
  return render(request,"home.html",{'products':products,'categories':data,'images':images})


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

@login_required(login_url='login')
def logout_view(request):
    logout(request)
    return redirect('login')

def read_cat(request,id):
    category1=category.objects.get(id=id)
    product=Product.objects.filter(category=category1)
    cate=category.objects.all()
    return render(request,"fruits.html",{'data':product,'cate':cate})

def product_details(request, id):
    item = get_object_or_404(Product, id=id)
    return render(request, "details.html", {'item': item})

def product_search(request):
    query = request.GET.get('q')
    if query:
        products = Product.objects.filter(product_name__icontains=query)
    else:
        products = Product.objects.all()
    return render(request, 'search.html', {'products': products, 'query': query})

@login_required(login_url='login')
def profile(request):
    try:
        # Use `request.user` directly since it's already a User instance.
        user = request.user
        # Use `get_object_or_404` to handle cases where the user might not be found.
        profile = get_object_or_404(User, username=user.username)
        return render(request, 'profile.html', {'profile': profile})
    except User.DoesNotExist:
        return HttpResponse("Profile not found", status=404)
    except Exception as e:
        return HttpResponse(f"An error occurred: {str(e)}", status=500)
    
@login_required(login_url='login')
def Add_cart(request,id):
    username=request.user
    product=get_object_or_404(Product,id=id)
    user1=User.objects.filter(email=username.email).first()
    print(user1)
    cart_item, created = CartItem.objects.get_or_create(product=product,user=user1)

    if not created:
        CartItem.quantity=CartItem.quantity+1
    else:
        CartItem.quantity=1

    return redirect('home')


def cart_view(request):
    items=CartItem.objects.all()
    total_price = sum(item.product.price * item.quantity for item in items)   
    return render(request, 'cart.html', {'items': items, 'total_price': total_price}) 













