"""Unit tests for the Wishlist model."""
from decimal import Decimal
from django.core.exceptions import ValidationError
from django.test import TestCase
from django.contrib.auth import get_user_model

from products.models import Product
from orders.models import Wishlist

User = get_user_model()

class WishlistModelTestCase(TestCase):
    """Unit tests for the Wishlist model."""

    def setUp(self):
        self.user = User.objects.create_user(
            username='wishlistuser',
            email='wishlist@example.com',
            password='wishlistpass'
        )
        self.product = Product.objects.create(
            name="Hydrating Toner",
            brand="ToneCare",
            price=Decimal("9.99"),
            description="Hydrates and tones skin.",
            HTU="Spray on face after cleansing.",
            COO="Canada"
        )
        self.wishlist = Wishlist.objects.create(
            user=self.user,
            product=self.product
        )

    def _assert_wishlist_is_valid(self):
        try:
            self.wishlist.full_clean()
        except ValidationError:
            self.fail("Test wishlist should be valid.")

    def _assert_wishlist_is_invalid(self):
        with self.assertRaises(ValidationError):
            self.wishlist.full_clean()

    def test_wishlist_is_valid_by_default(self):
        """Default wishlist is valid."""
        self._assert_wishlist_is_valid()

    def test_user_cannot_be_null(self):
        """Wishlist must have a user."""
        self.wishlist.user = None
        self._assert_wishlist_is_invalid()

    def test_product_cannot_be_null(self):
        """Wishlist must reference a Product."""
        self.wishlist.product = None
        self._assert_wishlist_is_invalid()

    def test_str_representation(self):
        """Check __str__ returns '<product.name> in Wishlist of <user.username>'."""
        expected_str = f"{self.product.name} in Wishlist of {self.user.username}"
        self.assertEqual(str(self.wishlist), expected_str)
