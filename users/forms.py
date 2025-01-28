from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate
from .models import User, Customer

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
    