from django.contrib.auth.models import AbstractUser, Group, Permission
from django.db import models

class User(AbstractUser):
    """Custom User model with roles for Customer and Admin."""
    email = models.EmailField(unique=True, blank=False)

    groups = models.ManyToManyField(
        Group,
        related_name="custom_user_groups",  
        blank=True,
    )
    user_permissions = models.ManyToManyField(
        Permission,
        related_name="custom_user_permissions",  
        blank=True,
    )
    
    class Role(models.TextChoices):
        CUSTOMER = 'customer', 'Customer'
        ADMIN = 'admin', 'Admin'

    role = models.CharField(
        max_length=10,
        choices=Role.choices,
        default=Role.CUSTOMER 
    )

    def is_customer(self):
        """Check if the user is a Customer."""
        return self.role == self.Role.CUSTOMER

    def is_admin(self):
        """Check if the user is an Admin."""
        return self.role == self.Role.ADMIN

    def __str__(self):
        return f"{self.first_name} {self.last_name} ({self.role})"


class Customer(models.Model):
    """Model to store additional customer-specific data."""
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="customer")
    preferred_skin_type = models.CharField(max_length=50, blank=True, null=True)

    def __str__(self):
        return f"Customer Profile: {self.user.first_name} {self.user.last_name}"


class Address(models.Model):
    """Model for storing user addresses."""
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="addresses")
    address_line_1 = models.CharField(max_length=150)
    address_line_2 = models.CharField(max_length=150, blank=True)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    postal_code = models.CharField(max_length=20)
    country = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    is_primary = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        if self.is_primary:
            Address.objects.filter(user=self.user, is_primary=True).update(is_primary=False)
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.address_line_1}, {self.city}, {self.country}"