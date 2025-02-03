from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.shortcuts import render, redirect
from .forms import UserLoginForm, UserRegistrationForm, UserProfileForm, UserAddressForm
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes
from django.contrib.auth.decorators import login_required
from .models import Address
from orders.models import Order, Wishlist

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

def logout_view(request):
    """Logs out the user and redirects to login page."""
    logout(request)
    return redirect("home")

def forgot_password(request):
    """View to handle user forgot password - inputting email for new password link"""
    if request.method == "POST":
        email = request.POST.get('email')
        try:
            user = User.objects.get(email=email)
            token = default_token_generator.make_token(user)
            uid = urlsafe_base64_encode(force_bytes(user.pk))
            reset_link = request.build_absolute_uri(f"/reset-password/{uid}/{token}/")

            # send the email
            send_mail(
                subject="Reset your password", 
                message=f"Click the link to reset your password: {reset_link}",
                from_email="noreply@gmail.com",
                recipient_list=[email],
            )
            messages.success(request, "A password reset link has been set to your email.")
            return redirect("login_view")
        except User.DoesNotExist:
            messages.error(request, "No account found with that email.")
    return render(request, 'users/forgot_password.html')


def reset_password(request, uidb64, token):
    """View to handle user forgot password - uses link from email to make new password"""    
    try:
        uid = force_bytes(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        if request.method == "POST":
            new_password = request.POST.get('new_password')
            confirm_password = request.POST.get('confirm_password')
            if new_password == confirm_password:
                user.set_password(new_password)
                user.save()
                messages.success(request, "Your password has been reset successfully!")
                return redirect("login_view")
            else:
                messages.error(request, "Passwords do not match.")
        return render(request, 'users/reset_password.html', {})
    else:
        messages.error(request, "The password reset link is invalid or has expired.")
        return redirect("forgot_password")

@login_required
def account_dashboard(request):
    """Displays the user account overview page"""
    return render(request, "users/account_dashboard.html", {"user": request.user})

@login_required
def profile(request):
    """Allows users to view and edit their profile information"""
    if request.method == "POST":
        form = UserProfileForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, "Your profile has been updated succcessfully!")
            return redirect("profile")
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        form = UserProfileForm(instance=request.user)

    return render(request, "users/profile.html", {"form": form})

@login_required
def address_list(request):
    """Displays the user's addresses and allows adding/editing"""
    addresses = Address.objects.filter(user=request.user)

    if request.method == "POST":
        form = UserAddressForm(request.POST)
        if form.is_valid():
            address = form.save(commit=False)
            address.user = request.user
            address.save()
            messages.success(request, "Address saved successfully!")
            return redirect("address_list")
    else:
        form = UserAddressForm()

    return render(request, "users/address_list.html", {"addresses": addresses, "form": form})

@login_required
def orders(request):
    """Displays user's past orders"""
    user_orders = Order.objects.filter(user=request.user).order_by("-created_at")
    
    if not user_orders:
        messages.info(request, "You have no past orders.")

    return render(request, "users/orders.html", {"orders": user_orders})    

@login_required
def wishlist(request):
    """Displays user's wishlist items"""
    wishlist_items = Wishlist.objects.filter(user=request.user)

    if not wishlist_items:
        messages.info(request, "Your wishlist is empty.")

    return render(request, "users/wishlist.html", {"wishlist_items": wishlist_items})
