from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate
from .models import User, Customer
from django.contrib.auth.models import User

class UserRegistrationForm(UserCreationForm):
    """Registration form for creating new users."""
    email = forms.EmailField(required=True)
    
    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name', 'password1', 'password2']
        
        def save(self, commit=True):
            user = super().save(commit=False)
            user.role = User.Role.CUSTOMER
            if commit:
                user.save()
                Customer.objects.create(
                    user=user,
                )
            return user
        
class UserLoginForm(forms.Form):
    """Login form for authenticating users."""
    username = forms.CharField(max_length=150, required=True)
    password = forms.CharField(widget=forms.PasswordInput, required=True)

    def clean(self):
        cleaned_data = super().clean()
        username = cleaned_data.get('username')
        password = cleaned_data.get('password')

        if username and password:
            user = authenticate(username=username, password=password)
            if user is None:
                raise forms.ValidationError("Invalid username or password")
        return cleaned_data
    
class UserProfileForm(forms.modelForm):
    """Form for updating user profile information"""
    phone_number = forms.CharField(max_length=15, required=False, label="Phone Number")

    class Meta:
        model = User
        fields = ["username", "email"]

class AddressForm(forms.ModelForm):
    """Form for adding/editing addresses"""
    class Meta:
        model = Address
        fields = [
            "address_line_1", "address_line2", "city", "state", 
            "postal_code", "country", "is_primary",
        ]

