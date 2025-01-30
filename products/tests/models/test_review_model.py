"""Unit tests for the Review model."""
from django.test import TestCase
from django.core.exceptions import ValidationError
from users.models import User
from products.models import Product, Review
from decimal import Decimal

class ReviewModelTestCase(TestCase):
    """Unit tests for the Review model."""

    def setUp(self):
        """Create a user, product, and associated review for testing."""
        self.user = User.objects.create_user(
            username="testuser",
            email="testuser@example.com",
            password="testpass"
        )
        self.product = Product.objects.create(
            name="Moisturizing Cream",
            brand="SkinCarePro",
            price=Decimal(19.99),
            description="A cream that deeply moisturizes.",
            HTU="Apply to the face and neck daily.",
            COO="France"
        )
        self.review = Review.objects.create(
            product=self.product,
            user=self.user,
            rating=4,
            comment="This cream is fantastic!"
        )

    def _assert_review_is_valid(self):
        """Helper to assert a review is valid."""
        try:
            self.review.full_clean()
        except ValidationError:
            self.fail("Test review should be valid.")

    def _assert_review_is_invalid(self):
        """Helper to assert a review is invalid."""
        with self.assertRaises(ValidationError):
            self.review.full_clean()

    def test_review_is_valid_by_default(self):
        """Ensure the default review is valid."""
        self._assert_review_is_valid()

    def test_review_requires_product(self):
        """Review must have a product."""
        self.review.product = None
        self._assert_review_is_invalid()

    def test_review_requires_user(self):
        """Review must have a user."""
        self.review.user = None
        self._assert_review_is_invalid()

    def test_rating_is_positive_small_integer(self):
        """Rating must be within the valid range for a PositiveSmallIntegerField (1–5)."""
        # Test that 0 is invalid
        self.review.rating = 0
        self._assert_review_is_invalid()

        # Test that 6 is invalid
        self.review.rating = 6
        self._assert_review_is_invalid()

        # Test that 1 is valid
        self.review.rating = 1
        self._assert_review_is_valid()

        # Test that 5 is valid
        self.review.rating = 5
        self._assert_review_is_valid()

    def test_comment_can_be_blank_or_null(self):
        """comment is optional (blank=True, null=True)."""
        self.review.comment = ""
        self._assert_review_is_valid()

        self.review.comment = None
        self._assert_review_is_valid()

    def test_unique_product_user_constraint(self):
        """User should not be able to leave more than one review per product."""
        # Attempt to create another review for the same product/user
        with self.assertRaises(Exception):  # Could be IntegrityError or ValidationError
            Review.objects.create(
                product=self.product,
                user=self.user,
                rating=5,
                comment="Another review for the same product."
            )

    def test_str_representation(self):
        """Check the string representation of Review."""
        expected_str = f"Review for {self.product.name} by {self.user.username}"
        self.assertEqual(str(self.review), expected_str)
