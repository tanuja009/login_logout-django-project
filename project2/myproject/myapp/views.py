from django.shortcuts import render

# Create your views here.
def home(request):
  return render(request,"homepage.html")
def add(request):
  return render(request,"addrecipe.html")