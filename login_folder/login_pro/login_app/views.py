from django.shortcuts import render,redirect
from django.contrib.auth import login,logout,authenticate
from .forms import *
# Create your views here.
def login(request):
    if request.method == 'POST':
        form = loginform(request.POST)
        if form.is_valid():
            # Extract credentials from the form
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')

            # Authenticate the user
            user = authenticate(request, username=username, password=password)
            
            if user is not None:
                # Log the user in
                login(request, user)
                return redirect('home')
            else:
                # If authentication fails, add an error to the form
                form.add_error(None, 'Invalid username or password')
    else:
        form = loginform()

    return render(request, 'login.html', {'form': form})
            
def registration(request):
    pass
def logout(request):
    logout(request)
    return redirect('login')
def home(request):
    pass