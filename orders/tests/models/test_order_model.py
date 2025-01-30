"""Unit tests for the Order model."""
from decimal import Decimal
from django.core.exceptions import ValidationError
from django.test import TestCase
from django.contrib.auth import get_user_model
from orders.models import Order

User = get_user_model()

class OrderModelTestCase(TestCase):
    """Unit tests for the Order model."""

    def setUp(self):
        self.user = User.objects.create_user(
            username='orderuser',
            email='orderuser@example.com',
            password='orderpass'
        )
        self.order = Order.objects.create(
            user=self.user,
            total_price=Decimal("99.99"),
            payment_status='pending',
        )

    def _assert_order_is_valid(self):
        try:
            self.order.full_clean()
        except ValidationError:
            self.fail("Test order should be valid.")

    def _assert_order_is_invalid(self):
        with self.assertRaises(ValidationError):
            self.order.full_clean()

    def test_order_is_valid_by_default(self):
        """Default setUp order should be valid."""
        self._assert_order_is_valid()

    def test_user_cannot_be_null(self):
        """Order must have a user."""
        self.order.user = None
        self._assert_order_is_invalid()

    def test_total_price_can_be_zero(self):
        """Order total_price defaults to 0.00 if not specified."""
        order2 = Order.objects.create(user=self.user)
        self.assertEqual(order2.total_price, Decimal("0.00"))

    def test_payment_status_defaults_to_pending(self):
        """Default payment_status should be 'pending'."""
        order2 = Order.objects.create(user=self.user)
        self.assertEqual(order2.payment_status, 'pending')

    def test_payment_status_can_be_completed(self):
        """Payment status can be changed to 'completed'."""
        self.order.payment_status = 'completed'
        self._assert_order_is_valid()

    def test_payment_status_invalid_raises_error(self):
        """Any status not in ('pending', 'completed') should fail validation."""
        self.order.payment_status = 'failed'
        self._assert_order_is_invalid()

    def test_str_representation(self):
        """Check __str__ returns 'Order <id> by <user>'."""
        expected_str = f"Order {self.order.id} by {self.user}"
        self.assertEqual(str(self.order), expected_str)
