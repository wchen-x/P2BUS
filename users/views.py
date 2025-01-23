from django.contrib.auth import login
from django.contrib import messages
from django.shortcuts import render, redirect
from .forms import UserRegistrationForm

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