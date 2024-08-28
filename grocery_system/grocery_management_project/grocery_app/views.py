from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.contrib.auth import authenticate, login,logout
from django.contrib.auth.decorators import login_required
from .forms import Product_Add_Form
from django.core.exceptions import ValidationError
from django.contrib.auth.forms import AuthenticationForm
from .models import *
from django.contrib.auth.models import User
import stripe
from django.conf import settings
from django.core.mail import send_mail
from django.http import JsonResponse
from django.views import View
# from django.contrib import messages

stripe.api_key = settings.STRIPE_SECRET_KEY


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
            send_mail(
                "Welcome Mail",
                "Welcome To Our Grocery World",
                "tapatidar@bestpeers.com",
                [user.email],
                fail_silently=False,
                    )
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
    categories=category.objects.all()

    return render(request,"about_us.html",{'categories':categories})

def Add_Product(request):
    if request.method == 'POST':
        form = Product_Add_Form(request.POST, request.FILES)
        categories=category.objects.all()
        if form.is_valid():
            form.save()
            user=Product.objects.all()
            return render(request,'home.html',{'user':user,'categories':categories})  # Redirect to the home page or any other page
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
    categories=category.objects.get(id=id)
    product=Product.objects.filter(category=categories)
    categories=category.objects.all()
    return render(request,"Readcart.html",{'data':product,'categories':categories})

def product_details(request, id):
    item = get_object_or_404(Product, id=id)
    categories=category.objects.all()

    return render(request, "details.html", {'item': item,'categories':categories})

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
        categories=category.objects.all()

        return render(request, 'profile.html', {'profile': profile,'categories':categories})
    except User.DoesNotExist:
        return HttpResponse("Profile not found", status=404)
    except Exception as e:
        return HttpResponse(f"An error occurred: {str(e)}", status=500)
    
@login_required(login_url='login')
def Add_cart(request,id):
    username=request.user
    product=get_object_or_404(Product,id=id)
    print(product)
    user1=User.objects.filter(email=username.email).first()
    cart_item, created = CartItem.objects.get_or_create(product=product,user=user1)

    if not created:
        cart_item.quantity += 1
    else:
        cart_item.quantity=1
    cart_item.save()
    items=CartItem.objects.filter(user=username)
    total_price = sum(item.product.price * item.quantity for item in items)  
    return render(request, 'cart.html', {'items': items, 'total_price': total_price}) 
    


def cart_view(request):
    username=request.user
    items=CartItem.objects.filter(user=username)
    categories=category.objects.all()
    shipping_charge=70
    total_price = sum(item.product.price * item.quantity for item in items)
    return render(request, 'cart.html', {'items': items, 'total_price': total_price, "categories":categories,'shipping_charge':shipping_charge}) 

@login_required(login_url="login")
def edit_profile(request,id):
    # if request.method == "POST":
    #     username = request.POST.get("username")
    #     email = request.POST.get("email")
    #     print("Ema    il is:", email)
    #     if email:
    #         update_data = User.objects.filter(email=email)
    #         print(update_data)
    #     else:
    #         update_data = User.objects.filter(id=id)
    #         print(update_data)
    #     print("Update data :", update_data)
    #     update_data.username = username
    #     update_data.save()
    #     return redirect("profile")

    
    
    if request.method == "POST":
        username= request.POST.get("username")
        email = request.POST.get("email")
        print("Email is:", email)
        # breakpoint()
        
        if email:
            update_data = User.objects.filter(email=email).first()
            print(update_data)  # Fetch the first matching user
        else:
            update_data = User.objects.filter(id=id).first() 
            print(update_data) # Fetch the first matching user by id
        
        if update_data:  # Check if the user was found
            print("Update data:", update_data)
            update_data.username = username
            update_data.save()
            return redirect("profile")
        else:
            return HttpResponse("data not found")
    else:
        user= request.user
        app_user = User.objects.get(username=user)
        categories= category.objects.all()
        return render(request, "edit_profile.html", {"profile": app_user,'categories':categories})
        # Handle the case where no user was found, e.g., by showing an error message


@login_required(login_url="login")
def Delete(request,id):
    user=User.objects.get(id=id)
    user.delete()
    return redirect('home')

@login_required(login_url="login")
def order_confirm(request, id):
    user=request.user
    order = get_object_or_404(Product, id=id)
    categories=category.objects.all()

    print(data)
    # Fetch the order or product based on the order_id
    # order, created = Order.objects.get_or_create(
    #     id=id,
    #     user=request.user,
    # )
    
    # # Fetch the product related to this order
    # product = order.product
    
    return render(request, 'order_confirm.html', {'data': order,'categories':categories})
@login_required(login_url="login")
def order(request,id):
    user=request.user
    order1= get_object_or_404(Product, id=id)
    order, is_created = Order.objects.get_or_create(product=order1,user=user)
    categories=category.objects.all()

    shipping_charge=70
    total_price=order.product.price + shipping_charge
    return render(request,'proceed_payment.html',{'order':order,'total_price':total_price,"shipping_charge":shipping_charge,'categories':categories})
    

@login_required(login_url="login")
def payment(request, id):
    user=request.user
    if id != "null":
        # Case 1: When an order ID is provided
        order = get_object_or_404(Order, id=id)
        if request.method == 'POST':
            try:
                # Access the related Product instance through the Order
                product = order.product
                shipping_charge=70
                # Create a Stripe Checkout Session
                session = stripe.checkout.Session.create(
                    payment_method_types=['card'],
                    line_items=[{
                        'price_data': {
                            'currency': 'inr',
                            'product_data': {
                                'name': product.product_name,  # Accessing product name correctly
                            },
                            'unit_amount': int(product.price * 100)+shipping_charge,  # Amount in paise (INR)
                        },
                        'quantity': 1,
                    }],
                    mode='payment',
                    success_url=request.build_absolute_uri('/payment_success/'),
                    cancel_url=request.build_absolute_uri('/payment_cancel/'),
                )
                
                return redirect(session.url, code=303)
            except stripe.error.StripeError as e:
                return JsonResponse({'error': f'Stripe error: {str(e)}'}, status=400)
            except Exception as e:
                return JsonResponse({'error': f'Error: {str(e)}'}, status=500)
        else:
            return JsonResponse({'error': 'Invalid request method'}, status=405)

    else:
        # Case 2: When no order ID is provided, process items in the cart
        items = CartItem.objects.filter(user=request.user)
        shipping_charge=70
        if request.method == 'POST':
            try:
                line_items = []
                
                for item in items:
                    product = item.product  # Access the product through each cart item
                    line_items.append({
                        'price_data': {
                            'currency': 'inr',
                            'product_data': {
                                'name': product.product_name,
                            },
                            'unit_amount': int(product.price * 100)+shipping_charge ,
                        },
                        'quantity': item.quantity,  # Assuming CartItem has a quantity field
                    })

                # Create a Stripe Checkout Session with all cart items
                session = stripe.checkout.Session.create(
                    payment_method_types=['card'],
                    line_items=line_items,
                    mode='payment',
                    success_url=request.build_absolute_uri('/payment_success/'),
                    cancel_url=request.build_absolute_uri('/payment_cancel/'),
                )

                return redirect(session.url, code=303)
            except stripe.error.StripeError as e:
                return JsonResponse({'error': f'Stripe error: {str(e)}'}, status=400)
            except Exception as e:
                return JsonResponse({'error': f'Error: {str(e)}'}, status=500)
        else:
            return JsonResponse({'error': 'Invalid request method'}, status=405)
        
# views.py
@login_required(login_url="login")
def payment_success(request):
    user=request.user
    send_mail(
                "thank you Mail",
                "thanks for order and your interest",
                "tapatidar@bestpeers.com",
                [user.email],
                fail_silently=False,
                    )
    return render(request, 'payment_success.html')
@login_required(login_url="login")
def payment_cancel(request):
    return render(request, 'home.html')

def order_list(request):
    # Fetch all orders for the logged-in user
    orders = Order.objects.filter(user=request.user)

    return render(request, 'order_list.html', {'orders': orders})


    
