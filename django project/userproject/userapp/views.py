from django.shortcuts import render,redirect,HttpResponse
from .forms import UserForm
from django.contrib.auth import login,logout
from django.contrib.auth.models import User
from django.views.generic import TemplateView,CreateView
# Create your views here.



# def user(request):
#     if request.method=='POST':
#         form=UserForm(request.POST)
#         if form.is_valid():
#             form.save()
#             return redirect("home")
       
#     else:
#         form=UserForm()
#     return render(request,"add.html",{'form':form})
# views.py

# class index(TemplateView):
#     template_name='home.html'


# # how to pass data in html from class based views 
# class add(TemplateView):
   
#     template_name='add.html'
#     def get_context_data(self, **kwargs):
#         array=['rohit','rahul','rashmika','ruchika']
#         dict={1:'small',2:'big',3:'large',4:'extra_large'}
#         age=22
#         # context_old=super().get_context_data(**kwargs)
#         context={'arr':array,'dict':dict,'age':age}
#         return context


# from django.http import HttpResponse
# from django.views import View


# class GreetingView(View):
#     greeting = "Good Day"
  

#     def get(self, request):
#         return HttpResponse(self.greeting)

def home(request):
    return render(request,"index.html")
