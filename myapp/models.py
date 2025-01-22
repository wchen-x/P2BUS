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
    """Model used for user authentication, and team member related information."""

    first_name = models.CharField(max_length=50, blank=False)
    last_name = models.CharField(max_length=50, blank=False)
    email = models.EmailField(unique=True, blank=False)
    

    class UserType(models.TextChoices):
        ADMIN = "admin", _("Admin")
        TUTOR = "tutor", _("Tutor")
        STUDENT = "student", _("Student")
    role = models.CharField(max_length=7, choices=UserType, default=UserType.STUDENT)

    class Meta:
        """Model options."""

        ordering = ['last_name', 'first_name']

    def save(self, *args, **kwargs):
        new_user = not self.pk
        super().save(*args, **kwargs)
        # If new user is created
        if new_user:
            # New admin and tutor accounts have to be approved
            if self.is_admin() or self.is_tutor():
                self.is_active = False
                self.save()
            # Create tutor or student record for relevant user
            if self.is_tutor():
                Tutor.objects.create(user_id=self, fee=10)
            elif self.is_student():
                Student.objects.create(user_id=self)

    def full_name(self):
        """Return a string containing the user's full name."""

        return f'{self.first_name} {self.last_name}'

    def gravatar(self, size=120):
        """Return a URL to the user's gravatar."""

        gravatar_object = Gravatar(self.email)
        gravatar_url = gravatar_object.get_image(size=size, default='robohash')
        return gravatar_url

    def mini_gravatar(self):
        """Return a URL to a miniature version of the user's gravatar."""

        return self.gravatar(size=60)

    def is_admin(self):
        """Return whether user is admin."""

        return self.role == self.UserType.ADMIN

    def is_tutor(self):
        """Return whether user is tutor."""

        return self.role == self.UserType.TUTOR

    def is_student(self):
        """Return whether user is student."""

        return self.role == self.UserType.STUDENT

class Tutor(models.Model):
    """ Model used to store Tutor expertise, availability and their fee/hour """

    user_id = models.OneToOneField(User, on_delete = models.CASCADE, related_name = "tutor_record", primary_key = True)

    expertise = models.JSONField(default = list)                                                                                    # Stores expertise as a list of known languages
    availability = models.JSONField(default = dict)                                                                                 #  & stores availability as dictionary of days of the week (Monday, Tuesday etc.) and then a list of times available
    
    fee = models.DecimalField(max_digits = 6, decimal_places = 2, default=0.0)

    def clean(self):
        super().clean()
        if self.fee <= 0:
            raise ValidationError("Fee must be greater than 0.")

    def username(self):
        """ Return the Tutor's associated username """

        return self.user_id.username

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

