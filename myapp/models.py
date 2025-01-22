from django.db import models

from django.core.validators import RegexValidator
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _
from django.utils.timezone import now
from libgravatar import Gravatar
from datetime import timedelta
from django.core.exceptions import ValidationError
    
class User(AbstractUser):
    """Model used for user authentication, and team member-related information."""

    first_name = models.CharField(max_length=50, blank=False)
    last_name = models.CharField(max_length=50, blank=False)
    email = models.EmailField(unique=True, blank=False)
    
    class Role(models.TextChoices):
        CUSTOMER = 'custom4er', 'Customer'
        ADMIN = 'admin', 'Admin'
        
    role = models.CharField(
        max_length=10,
        choices=Role.choices,
        default=Role.CUSTOMER
    )

    class Meta:
        """Model options."""
        ordering = ['last_name', 'first_name']
        
    def is_admin(self):
        """Return whether user is admin."""
        return self.role == self.Role.ADMIN
    
    def is_customer(self):
        """"Return whether user is customer."""
        return self.role == self.Role.CUSTOMER

    def __str__(self):
        return f"{self.first_name} {self.last_name} ({self.get_role_display()})"

class Product:
    pass

class Wishlist:
    pass

class Order(models.Model):
    """ Model to store order information"""
    order_id = models.AutoField(primary_key=True)   # Order number automatically increments when created and is assigned as the primary key
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="orders")
    product = models.ManyToMany(Product, through='OrderItem')
    address = models.ForeignKey(Address, on_delete=models.CASCADE, related_name="orders")
    total_price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    payment_status = models.CharField(
        max_length=20,
        choices=[
            ('pending', 'Pending'),
            ('completed', 'Completed'),
            ('failed', 'Failed'),
            ('refunded', 'Refunded'),
        ],
        default='pending',
    )
    fulfillment_status = models.CharField(
        max_length=20,
        choices=[
            ('pending', 'Pending'),
            ('processing', 'Processing'),
            ('completed', 'Completed'),
            ('cancelled', 'Cancelled'),
        ],
        default='pending',
        )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Order {self.order_id} by {self.user.first_name} {self.user.last_name} on {self.created_at}"

class OrderItem(models.Model):
    """Intermediate table to represent products in an order"""
    orderItem_id = models.AutoField(primary_key=True)
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    price_per_unit = models.DecimalField(max_digits=10, decimal_places=2)
    subtotal = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.quantity} x {self.product.name} in Order {self.order.order_id}"

class Address(models.Model):
    """Model for storing user addresses"""
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="addresses", null=True, blank=True)
    address_line_1 = models.CharField(max_length=150) 
    address_line_2 = models.CharField(max_length=150)   # Apartment number, floor etc
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    postal_code = models.CharField(max_length=20)
    country=models.CharField(max_length=100)
    phone_number = models.CharField(max_length=15, blank=True, null=True)   # Optional phone number
    is_primary = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.address_line_2}, {self.address_line_1}, {self.city}, {self.state}, {self.postal_code}, {self.country}"

class Review(models.Model):
    review_id = models.AutoField(primary_key=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="reviews")
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="reviews")
    rating = models.PositiveSmallIntegerField()
    comment = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class meta:
        # Ensures user can leave only one review per product
        constraints = [
            models.UniqueConstraint(fields=['product', 'user'], name='unique_product_user_review')
        ]
    
    def __str__(self):
        return f"Review by {self.user.first_name} {self.user.last_name} for {self.product.name} - {self.rating} stars"

