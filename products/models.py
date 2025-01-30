from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from users.models import User

class Product(models.Model):
    """Model to store product information."""
    name = models.CharField(max_length=255, blank=False)
    brand = models.CharField(max_length=50, blank=False)
    price = models.DecimalField(max_digits=6, decimal_places=2, default=0.00)
    description = models.CharField(max_length=500, blank=False)
    HTU = models.CharField(max_length=500, blank=False)  # How to use
    COO = models.CharField(max_length=50, blank=False)  # Country of origin
    in_stock = models.BooleanField(default=True)
    image = models.ImageField(upload_to='product_images/', blank=True, null=True)

    def __str__(self):
        return self.name


class Review(models.Model):
    """Model for storing product reviews."""
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="reviews")
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="reviews")
    rating = models.PositiveSmallIntegerField(
        validators=[
            MinValueValidator(1),
            MaxValueValidator(5)
        ]
    )
    comment = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['product', 'user'], name='unique_product_user_review')
        ]

    def __str__(self):
        return f"Review for {self.product.name} by {self.user.username}"
