"""Unit tests for the Order Item model."""
from decimal import Decimal
from django.core.exceptions import ValidationError
from django.test import TestCase
from django.contrib.auth import get_user_model

from products.models import Product
from orders.models import Order, OrderItem

User = get_user_model()

class OrderItemModelTestCase(TestCase):
    """Unit tests for the OrderItem model."""

    def setUp(self):
        self.user = User.objects.create_user(
            username='itemuser',
            email='itemuser@example.com',
            password='itempass'
        )
        self.product = Product.objects.create(
            name="Facial Cleanser",
            brand="CleanBrand",
            price=Decimal("12.99"),
            description="Cleans your face effectively.",
            HTU="Apply to wet face and rinse.",
            COO="USA"
        )
        self.order = Order.objects.create(
            user=self.user,
            total_price=Decimal("0.00"),
            payment_status='pending'
        )
        self.order_item = OrderItem.objects.create(
            order=self.order,
            product=self.product,
            quantity=2,
            price_per_unit=Decimal("12.99")
        )

    def _assert_orderitem_is_valid(self):
        try:
            self.order_item.full_clean()
        except ValidationError:
            self.fail("Test order_item should be valid.")

    def _assert_orderitem_is_invalid(self):
        with self.assertRaises(ValidationError):
            self.order_item.full_clean()

    def test_order_item_is_valid_by_default(self):
        """Default OrderItem should be valid."""
        self._assert_orderitem_is_valid()

    def test_order_cannot_be_null(self):
        """OrderItem must belong to an Order."""
        self.order_item.order = None
        self._assert_orderitem_is_invalid()

    def test_product_cannot_be_null(self):
        """OrderItem must reference a Product."""
        self.order_item.product = None
        self._assert_orderitem_is_invalid()

    def test_quantity_default_is_one(self):
        """If quantity isn't specified, it should default to 1."""
        item2 = OrderItem.objects.create(
            order=self.order,
            product=self.product,
            price_per_unit=Decimal("12.99")
        )
        self.assertEqual(item2.quantity, 1)

    def test_quantity_cannot_be_zero_or_negative(self):
        """
        A quantity <= 0 should fail validation IF you have
        a custom validator or use PositiveIntegerField.

        If you only used `models.PositiveIntegerField(...)`
        for `quantity`, zero or negative would raise an error.
        """
        self.order_item.quantity = 0
        self._assert_orderitem_is_invalid()

        self.order_item.quantity = -5
        self._assert_orderitem_is_invalid()

    def test_price_per_unit_can_be_decimal(self):
        """price_per_unit can store decimals up to 10 digits, 2 decimal places."""
        self.order_item.price_per_unit = Decimal("1000.50")
        self._assert_orderitem_is_valid()

    def test_str_representation(self):
        """Check __str__ returns '<quantity> x <product.name> in Order <id>'."""
        expected_str = f"2 x Facial Cleanser in Order {self.order.id}"
        self.assertEqual(str(self.order_item), expected_str)
