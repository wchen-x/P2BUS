from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User

class UserRegistrationForm(UserCreationForm):
    """Registration form for  creating new users."""
    email = forms.EmailField(required=True)
    
    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name', 'password1', 'password2']
        
        def save(self, commit=True):
            user = super().save(commit=False)
            user.role = User.Role.CUSTOMER
            if commit:
                user.save()
            return user