"""Unit tests for the Address model."""
from django.core.exceptions import ValidationError
from django.test import TestCase
from django.contrib.auth import get_user_model
from users.models import Address, User

class AddressModelTestCase(TestCase):
    """Unit tests for the Address model."""

    def setUp(self):
        self.user = User.objects.create_user(
            username='addruser',
            email='addr@example.com',
            password='testpass'
        )
        self.address1 = Address.objects.create(
            user=self.user,
            address_line_1='123 Test Street',
            address_line_2='Apt 4',
            city='Testville',
            state='TS',
            postal_code='12345',
            country='Testland',
            phone_number='555-1234',
            is_primary=True
        )
        self.address2 = Address.objects.create(
            user=self.user,
            address_line_1='456 Another Road',
            address_line_2='',
            city='Anotherville',
            state='AT',
            postal_code='67890',
            country='Anotherland',
            is_primary=False
        )

    def _assert_address_is_valid(self, address):
        try:
            address.full_clean()
        except ValidationError:
            self.fail('Address should be valid.')

    def _assert_address_is_invalid(self, address):
        with self.assertRaises(ValidationError):
            address.full_clean()

    def test_address_is_valid_by_default(self):
        """address1 should be valid with all required fields."""
        self._assert_address_is_valid(self.address1)

    def test_address_line_1_cannot_be_blank(self):
        """address_line_1 is a required field."""
        self.address1.address_line_1 = ''
        self._assert_address_is_invalid(self.address1)

    def test_city_cannot_be_blank(self):
        self.address1.city = ''
        self._assert_address_is_invalid(self.address1)

    def test_state_cannot_be_blank(self):
        self.address1.state = ''
        self._assert_address_is_invalid(self.address1)

    def test_postal_code_cannot_be_blank(self):
        self.address1.postal_code = ''
        self._assert_address_is_invalid(self.address1)

    def test_country_cannot_be_blank(self):
        self.address1.country = ''
        self._assert_address_is_invalid(self.address1)

    def test_phone_number_can_be_blank(self):
        """phone_number is optional."""
        self.address1.phone_number = ''
        self._assert_address_is_valid(self.address1)

    def test_phone_number_can_be_null(self):
        """phone_number can be null."""
        self.address1.phone_number = None
        self._assert_address_is_valid(self.address1)

    def test_setting_new_primary_address(self):
        """
        When a new address is set to is_primary=True,
        the old one should become is_primary=False.
        """
        self.address2.is_primary = True
        self.address2.save()

        self.address1.refresh_from_db()
        self.address2.refresh_from_db()

        self.assertFalse(self.address1.is_primary)
        self.assertTrue(self.address2.is_primary)

    def test_str_representation(self):
        """Check string representation for the Address model."""
        expected_str = '123 Test Street, Testville, Testland'
        self.assertEqual(str(self.address1), expected_str)