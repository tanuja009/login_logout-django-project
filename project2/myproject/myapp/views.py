from django.shortcuts import render,redirect,HttpResponse
from .models import Recipe
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.models import User
# Create your views here.
@login_required(login_url='login')
def home(request):
  s=Recipe.objects.all()
  return render(request,"homepage.html",{'sdata':s})

@login_required(login_url='login')
def add(request):
    if request.method == 'POST':
        # Extract data from the form
        name = request.POST.get('name')
        desc = request.POST.get('description')
        image = request.FILES.get('image')  # Use request.FILES for file uploads

        # Create a new Recipe object
        Recipe.objects.create(
            recipe_name=name,
            recipe_description=desc,
            recipe_image=image
        )

        # Optionally print or log for debugging
        print(f"Added recipe: {name}, {desc}, {image}")

        # Redirect to the home page or any other page
        return redirect('home')
    else:
        # If the request method is GET, render the form template
        return render(request, 'addrecipe.html')
    
def login_view(request):
    if request.method=='POST':
        username=request.POST.get('username')
        pass1=request.POST.get('pass')
        user=authenticate(request,username=username,password=pass1)
        if user is not None:
            print(user)
            login(request,user)
            return redirect('home')
        else:
            # messages.ERROR(request,"user name password are wrong")
            return redirect('login')
        

    return render (request,'login.html')




def signup_view(request):
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

def logout_view(request):
    logout(request)
    return redirect('login')

