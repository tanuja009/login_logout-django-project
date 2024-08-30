from django.shortcuts import render,redirect
from .models import Student
from .forms import Userform
from django.contrib.auth.forms import UserCreationForm,AuthenticationForm;
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login,logout
# Create your views here.

@login_required(login_url='login')
def Home(request):
    std=Student.objects.all()
    return render(request,'index.html',{'std':std})

@login_required(login_url='login')
def Add(request):
    if request.method=='POST':
        form = Userform(request.POST)
        print(form)
        if form.is_valid():
            form.save()
            return redirect('home')
        else:
            return render(request,"login.html",{"error":'invalid credential'})
    else:
        form = Userform()
    return render(request,'add.html',{"form": form})
            
@login_required(login_url='login')
def Delete(request,id):
    s=Student.objects.get(pk=id)
    s.delete()
    return redirect('home')

@login_required(login_url='login')
def update(request,id):
    s=Student.objects.get(pk=id)
    return render(request,"update.html",{'std':s})
        
def do_update(request,id):
    name=request.POST.get('name')
    email=request.POST.get('email')
    address=request.POST.get('address')
    contact=request.POST.get('contact')
    std=Student.objects.get(pk=id)
    std.name=name
    std.email=email
    std.address=address
    std.contact=contact
    std.save()
    return redirect('home')


# def Userforms(request):
#     return render(request,"forms.html")

def register_view(request):
    if request.method=='POST':
       name=request.POST.get('username')
       passwords=request.POST.get('password')
    #    form=UserCreationForm(request.POST)
       if form.is_valid():
           user=form.save()
        #    login(request,user)
           return redirect('login')
    else:
        form=UserCreationForm()
    return render(request,"register.html",{'form':form})

        


def login_view(request):
    if request.method=='POST':
    #    form=AuthenticationForm(request,data=request.POST)
       if form.is_valid():
           user=form.get_user()
           login(request,user)
           return redirect('home')
    else:
        initial_data={'username':'','password':''}
        form=AuthenticationForm(initial=initial_data)
    return render(request,"login.html",{'form':form})
        
def logout_view(request):
    logout(request)
    return redirect('login')