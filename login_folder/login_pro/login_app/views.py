from django.shortcuts import render,redirect
from django.contrib.auth import login,logout,authenticate
from .forms import *
# Create your views here.
def login(request):
    if request.method=='POST':
        form=loginform(request.POST)
        if form.is_valid():
            user=form.save()
            login(request,user)
            return redirect('home')
        else:
            return render(request,"login.html",{'error':'credential error'})
    else:
        form=loginform()
    return render(request,"login.html",{'form':form})
            
def registration(request):
    pass
def logout(request):
    logout(request)
    return redirect('login')
def home(request):
    pass