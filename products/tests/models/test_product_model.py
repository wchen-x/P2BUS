"""Unit tests for the Product model."""
from django.test import TestCase
from django.core.exceptions import ValidationError
from products.models import Product
from decimal import Decimal

class ProductModelTestCase(TestCase):
    """Unit tests for the Product model."""

    def setUp(self):
        """Create a Product instance to use in tests."""
        self.product = Product.objects.create(
            name="Super Serum",
            brand="SkinCarePro",
            price=Decimal("29.99"),
            description="A serum that hydrates and revitalizes the skin.",
            HTU="Apply a few drops to clean skin and massage gently.",
            COO="USA",
            in_stock=True,
            image=None  # optional
        )

    def _assert_product_is_valid(self):
        """Helper to assert a product is valid."""
        try:
            self.product.full_clean()
        except ValidationError:
            self.fail("Test product should be valid.")

    def _assert_product_is_invalid(self):
        """Helper to assert a product is invalid."""
        with self.assertRaises(ValidationError):
            self.product.full_clean()

    def test_product_is_valid_by_default(self):
        """Ensure the default product created in setUp is valid."""
        self._assert_product_is_valid()

    def test_name_cannot_be_blank(self):
        """Name must not be empty."""
        self.product.name = ""
        self._assert_product_is_invalid()

    def test_brand_cannot_be_blank(self):
        """Brand must not be empty."""
        self.product.brand = ""
        self._assert_product_is_invalid()

    def test_price_defaults_to_zero(self):
        """
        By default, if no price is given, it should be 0.00.
        (We assigned 29.99 in setUp, but you can test the default scenario if you like)
        """
        product2 = Product.objects.create(
            name="Test Product",
            brand="Test Brand",
            description="Test description",
            HTU="Test HTU",
            COO="Testland"
        )
        self.assertEqual(product2.price, 0.00)

    def test_description_cannot_be_blank(self):
        """Description must not be empty."""
        self.product.description = ""
        self._assert_product_is_invalid()

    def test_HTU_cannot_be_blank(self):
        """HTU must not be empty."""
        self.product.HTU = ""
        self._assert_product_is_invalid()

    def test_COO_cannot_be_blank(self):
        """COO must not be empty."""
        self.product.COO = ""
        self._assert_product_is_invalid()

    def test_in_stock_default_is_true(self):
        """Check default of in_stock is True."""
        product2 = Product.objects.create(
            name="Another Product",
            brand="BrandX",
            description="Desc",
            HTU="Use it well",
            COO="Somewhere"
        )
        self.assertTrue(product2.in_stock)

    def test_str_representation(self):
        """Check the string representation of Product."""
        self.assertEqual(str(self.product), "Super Serum")
