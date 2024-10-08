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
from django.contrib.auth.models import AnonymousUser
from django.contrib.auth.mixins import LoginRequiredMixin
import logging
# from django.contrib import messages

stripe.api_key = settings.STRIPE_SECRET_KEY

class SignupPage(View):
    def get(self,request):
        return render(request,'signup.html')
    
    def post(self,request):
        
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


class LoginPage(View):
    def get(self, request):
        return render(request, 'login.html')
    
    def post(self, request):
        username = request.POST.get('username')
        password = request.POST.get('pass')
        # Check if username and password are provided
        if not username or not password:
            
            return redirect('login')

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            print(user.email)
            try:
                send_mail(
                "Welcome Mail",
                "Welcome To Our Grocery World",
                settings.EMAIL_HOST_USER,  # Ensure this is correctly set in settings.py
                [user.email],
                fail_silently=False,
                )
                print("Email sent successfully.")
            except Exception as e:
                return HttpResponse("error")
            return redirect('home')
        else:
           
            return redirect('login')
        
class HomePage(View):
    def get(self,request):
        products =Product.objects.all()
        data=category.objects.all()
        images = [
        "https://cdn.pixabay.com/photo/2022/08/01/07/59/vegetables-7357585_640.png",
        "https://5.imimg.com/data5/MG/FQ/SA/SELLER-283756/all-fmcg-grocery-products.jpg",
        "https://media.istockphoto.com/id/171302954/photo/groceries.jpg?s=612x612&w=0&k=20&c=D3MmhT5DafwimcYyxCYXqXMxr1W25wZnyUf4PF1RYw8="
        ]
        #carousal_image=Product.objects.values_list('carousal_image', flat=True)
        return render(request,"home.html",{'products':products,'categories':data,'images':images})
    

class AboutPage(View):   
    def get(self,request):
        categories=category.objects.all()
        return render(request,"about_us.html",{'categories':categories})
    

class Add_Product(LoginRequiredMixin,View):
    login_url = 'login' 
    def get(self,request):
        form = Product_Add_Form()
        return render(request, 'add.html', {'form':form})
    
    def post(self,request):
            form = Product_Add_Form(request.POST, request.FILES)
            categories=category.objects.all()
            if form.is_valid():
                form.save()
                user=Product.objects.all()
                return render(request,'home.html',{'user':user,'categories':categories})  # Redirect to the home page or any other page
       

class LogoutPage(LoginRequiredMixin,View):
    # @login_required(login_url='login')
    login_url = 'login' 
    def get(self,request):
        logout(request)
        return redirect('login')
    
class ReadProduct(LoginRequiredMixin,View):
    login_url = 'login' 
    def get(self,request,id):
        categories=category.objects.get(id=id)
        product=Product.objects.filter(category=categories)
        categories=category.objects.all()
        return render(request,"Readcart.html",{'data':product,'categories':categories})


class ProductDetails(LoginRequiredMixin,View):
    login_url = 'login' 
    def get(self,request, id):
        item = get_object_or_404(Product, id=id)
        categories=category.objects.all()
        return render(request, "details.html", {'item': item,'categories':categories})
    
class ProductSearch(LoginRequiredMixin,View):
    login_url = 'login' 
    def get(self,request):
        query = request.GET.get('q','')
        if query:
            products = Product.objects.filter(product_name__icontains=query)
        else:
            products = Product.objects.all()
        return render(request, 'search.html', {'products': products, 'query': query})
    
    
# @login_required(login_url='login')
class AddCart(LoginRequiredMixin, View):
    login_url = 'login'

    def post(self, request, id):
        user = request.user  # Changed username to user for clarity
        product = get_object_or_404(Product, id=id)  # Fetch product or return 404
        print(f"Product: {product}")  # Debug print

        # Get or create cart item
        cart_item, created = CartItem.objects.get_or_create(product=product, user=user)

        if not created:
            cart_item.quantity += 1  # Increment quantity if cart item exists
        else:
            cart_item.quantity = 1  # Set quantity to 1 for new cart item
        
        cart_item.save()  # Save the cart item

        # Fetch all items in the user's cart and calculate total price
        items = CartItem.objects.filter(user=user)
        total_price = sum(item.product.price * item.quantity for item in items)

        # Render the cart template with updated cart items and total price
        return render(request, 'cart.html', {
            'items': items,
            'total_price': total_price
        })

class CartView(LoginRequiredMixin, View):
    login_url = 'login'

    def get(self, request):
        try:
            username = request.user
            print(f"Username: {username}")  # Debug print
            items = CartItem.objects.filter(user=username)
            print(f"Items: {items}")  # Debug print
            categories = category.objects.all()
            shipping_charge = 70
            total_price = sum(item.product.price * item.quantity for item in items)
            print(f"Total Price: {total_price}")  # Debug print
            return render(request, 'cart.html', {
                'items': items,
                'total_price': total_price,
                'categories': categories,
                'shipping_charge': shipping_charge
            })
        except Exception as e:
            logging.error(f"Error in CartView: {e}")
            return HttpResponse(f"Error: {e}")

class DeleteCartItem(LoginRequiredMixin,View):
    login_url = 'login'
    def get(self,request,id):
        username=request.user
        item=CartItem.objects.filter(id=id)
        item.delete()
        items=CartItem.objects.filter(user=username)
        return render(request,'cart.html',{'items': items})           
    

# @login_required(login_url='login')
class Profile(LoginRequiredMixin,View):
    login_url = 'login'
    def get(self,request):
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

class EditProfile(LoginRequiredMixin,View):
    login_url = 'login'  
    def get(self, request, id=None):
        user = request.user
        app_user = User.objects.get(username=user)
        categories = category.objects.all()
        return render(request, "edit_profile.html", {"profile": app_user, 'categories': categories})

    def post(self, request, id):
        username = request.POST.get("username")
        email = request.POST.get("email")
        print("Email is:", email)

        if email:
            update_data = User.objects.filter(email=email).first()
        else:
            update_data = User.objects.filter(id=id).first()

        if update_data:  # Check if the user was found
            print("Update data:", update_data)
            update_data.username = username
            update_data.save()
            return redirect("profile")
        else:
            return HttpResponse("Data not found")
            
           


class Delete(LoginRequiredMixin, View):
    login_url = 'login'

    def get(self, request, id):
        user = User.objects.get(id=id)
        user.delete()
        return redirect('home')

class OrderView(LoginRequiredMixin,View):
    login_url = 'login'
    def get(self,request, id):
        user=request.user
        order = get_object_or_404(Product, id=id)
        categories=category.objects.all()

        print(data)
        return render(request, 'order_confirm.html', {'data': order,'categories':categories})
    
    
class Order1(LoginRequiredMixin,View):
    login_url = 'login'
    def get(self, request, id):
        # Check if the user is authenticated
        if isinstance(request.user,AnonymousUser):
            # Redirect to login page or show an error message
            return redirect('login')  # Replace 'login' with your actual login view name

        user = request.user
        product = get_object_or_404(Product, id=id)
        order, is_created = Order.objects.get_or_create(product=product, user=user)
        categories = category.objects.all()

        shipping_charge = 70
        total_price = order.product.price + shipping_charge
        
        return render(request, 'proceed_payment.html', {
            'order': order,
            'total_price': total_price,
            'shipping_charge': shipping_charge,
            'categories': categories
        })
    

class PaymentModule(View):
    def get(self,request):
         return JsonResponse({'error': 'Invalid request method'}, status=405)
    def post(self,request, id):
        user=request.user
        if id != "null":
            # Case 1: When an order ID is provided
            order = get_object_or_404(Order, id=id)
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
                                'unit_amount': int(product.price * 100)+(shipping_charge*100),  # Amount in paise (INR)
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
                                'unit_amount': int(product.price * 100)+(shipping_charge*100) ,
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
class Payment_success(View):
    def get(self,request):
        user=request.user
        send_mail(
                    "thank you Mail",
                    "thanks for order and your interest",
                    "tapatidar@bestpeers.com",
                    [user.email],
                    fail_silently=False,
                        )
        return render(request, 'payment_success.html')


class payment_cancel(View):
    def get(self,request):
        return render(request, 'home.html')

class Order_List(View):
    def get(self,request):
        # Fetch all orders for the logged-in user
        orders = Order.objects.filter(user=request.user)

        return render(request, 'order_list.html', {'orders': orders})


    
