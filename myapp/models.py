from django.db import models
from django.contrib.auth.models import AbstractUser, Group, Permission
from django.utils.timezone import now
from datetime import timedelta
from django.core.exceptions import ValidationError


class Product(models.Model):
    """Model to store product information."""
    name = models.CharField(max_length=255, blank=False)
    brand =  models.CharField(max_length=50, blank=False)
    price = models.DecimalField(max_digits=6, decimal_places=2, default=0.00)
    description = models.CharField(max_length=500, blank=False)
    HTU = models.CharField(max_length=500, blank=False) # how to use
    COO =  models.CharField(max_length=50, blank=False) # country of origin
    
    class Category(models.TextChoices):
        SKINCARE = 'skincare', 'Skincare'
        HAIRBODY = 'hair&body', 'Hair & Body'
        MAKEUP = 'makeup', 'Makeup'
        NECESSITIES = 'necessities', 'Necessities'
        
    category =  models.CharField(
        max_length=20,
        choices=Category.choices
    )
    
    image = models.ImageField(upload_to='product_images/', blank=True, null=True)
    in_stock = models.BooleanField(default=False) # whether product is in stock or not
    
    def clean(self):
        super().clean()
        if self.price <= 0:
            raise ValidationError("Price must be greater than 0.")
        
    def __str__(self):
        return self.name    
    
    


class Order(models.Model):
    """Model to store order information."""
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="orders")
    product = models.ManyToManyField(Product, through='OrderItem')
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
        return f"Order {self.id} by {self.user.first_name} {self.user.last_name} on {self.created_at.strftime('%Y-%m-%d')}"


class OrderItem(models.Model):
    """Intermediate table to represent products in an order."""
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    price_per_unit = models.DecimalField(max_digits=10, decimal_places=2)
    subtotal = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)

    def save(self, *args, **kwargs):
        self.subtotal = self.quantity * self.price_per_unit
        super().save(*args, **kwargs)   
 
    def __str__(self):
        return f"{self.quantity} x {self.product.name} in Order {self.order.id}"


class Review(models.Model):
    """Model for storing reviews."""
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="reviews")
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="reviews")
    rating = models.PositiveSmallIntegerField()
    comment = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        # Ensures user can leave only one review per product
        constraints = [
            models.UniqueConstraint(fields=['product', 'user'], name='unique_product_user_review')
        ]


    def __str__(self):
        return f"Review by {self.user.first_name} {self.user.last_name} for {self.product.name} - {self.rating} stars"


class Wishlist(models.Model):
    """Model to store customer wishlists."""
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="wishlists")
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="wishlists")
    quantity = models.PositiveIntegerField(default=1)
    
    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['user', 'product'], name='unique_user_product_wishlist')
        ]
    