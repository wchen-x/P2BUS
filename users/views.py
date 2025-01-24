from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.shortcuts import render, redirect
from .forms import UserLoginForm, UserRegistrationForm

def register(request):
    """View to handle user registration."""
    if request.method == "POST":
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save() 
            login(request, user)
            messages.success(request, "Registration successful!")
            return redirect("home")
        else:
            messages.error(request, "Registration failed. Please correct the errors below.")
    else:
        form = UserRegistrationForm()

    return render(request, 'users/register.html', {'form': form})

def login_view(request):
    """View to handle user login"""
    if request.method == "POST":
        form = UserLoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect("home") 
    else:
        form = UserLoginForm()
    return render(request, 'users/login.html', {'form': form})
