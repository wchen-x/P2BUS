"""Unit tests for the Customer User model."""
from django.core.exceptions import ValidationError
from django.test import TestCase
from django.contrib.auth import get_user_model
from users.models import Customer, User

class CustomerModelTestCase(TestCase):
    """Unit tests for the Customer model."""

    def setUp(self):
        # Create a user and its associated customer profile
        self.user = User.objects.create_user(
            username='customeruser',
            email='customer@example.com',
            password='testpass'
        )
        self.customer = Customer.objects.create(
            user=self.user,
            preferred_skin_type='Dry'
        )

    def _assert_customer_is_valid(self):
        try:
            self.customer.full_clean()
        except ValidationError:
            self.fail('Test customer should be valid.')

    def _assert_customer_is_invalid(self):
        with self.assertRaises(ValidationError):
            self.customer.full_clean()

    def test_customer_is_valid_by_default(self):
        """Customer with all valid fields should be valid."""
        self._assert_customer_is_valid()

    def test_preferred_skin_type_can_be_blank(self):
        """preferred_skin_type can be blank."""
        self.customer.preferred_skin_type = ''
        self._assert_customer_is_valid()

    def test_preferred_skin_type_can_be_null(self):
        """preferred_skin_type can be null."""
        self.customer.preferred_skin_type = None
        self._assert_customer_is_valid()

    def test_str_representation(self):
        """Check the string representation of the Customer model."""
        self.user.first_name = 'Jane'
        self.user.last_name = 'Smith'
        self.user.save()
        self.assertEqual(
            str(self.customer),
            'Customer Profile: Jane Smith'
        )
