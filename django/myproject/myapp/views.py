from django.shortcuts import render
from django.views import View
from .forms import userform
# Create your views here.
from django.shortcuts import render,HttpResponse,redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages

# Create your views here.
@login_required(login_url='login')
def HomePage(request):
    return render (request,'home.html')

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

def LogoutPage(request):
    logout(request)
    return redirect('login')

class reset(View):
    def get(self,request):
        form=userform()
        return render(request,"reset.html",{'form':form})
    
    def post(self, request, *args, **kwargs):
        form = userform(request.POST)
        
        if form.is_valid():
            email = form.cleaned_data.get('email')
            password = form.cleaned_data.get('password')
            
            try:
                user = User.objects.get(email=email)
                user.set_password(password)  
                user.save()
                return redirect('login')   
            except User.DoesNotExist:
               
                return render(request, 'reset.html', {'form': form, 'error': 'User with this email does not exist'})
        else:
            
            return render(request, 'reset.html', {'form': form})