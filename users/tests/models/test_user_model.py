"""Unit tests for the User model."""
from django.core.exceptions import ValidationError
from django.test import TestCase
from django.contrib.auth import get_user_model
from users.models import User

class UserModelTestCase(TestCase):
    """Unit tests for the Custom User model."""
    
    def setUp(self):
        # create a basic user; override fields in tests as needed
        self.user = User.objects.create_user(
            username='testuser',
            email='testuser@exaple.com',
            password='testpass'
        )
        
    def _assert_user_is_valid(self):
        try:
            self.user.full_clean()
        except:
            self.fail('Test user should be valid.')
        
    def _assert_user_is_invalid(self):
        with self.assertRaises(ValidationError):
            self.user.full_clean()

    def test_user_is_valid_by_default(self):
        """Ensure that the default user with required fields is valid."""
        self._assert_user_is_valid()

    def test_email_cannot_be_blank(self):
        """Email must not be empty."""
        self.user.email = ''
        self._assert_user_is_invalid()
        
    def test_email_must_be_unique(self):
        """Email must be unique across users."""
        User.objects.create_user(
            username='anotheruser',
            email='another@example.com',
            password='testpass'
        )
        self.user.email = 'another@example.com'
        self._assert_user_is_invalid()

    def test_default_role_is_customer(self):
        """Ensure that the default role for new users is 'customer'."""
        self.assertEqual(self.user.role, User.Role.CUSTOMER)

    def test_role_can_be_admin(self):
        """Role can be set to 'admin'."""
        self.user.role = User.Role.ADMIN
        self._assert_user_is_valid()

    def test_invalid_role_raises_error(self):
        """An invalid role choice should fail validation."""
        self.user.role = 'invalid_role'
        self._assert_user_is_invalid()
        
    def test_is_customer_method(self):
        """is_customer() returns True if role is 'customer'."""
        self.assertTrue(self.user.is_customer())
        self.user.role = User.Role.ADMIN
        self.assertFalse(self.user.is_customer())

    def test_is_admin_method(self):
        """is_admin() returns True if role is 'admin'."""
        self.assertFalse(self.user.is_admin())
        self.user.role = User.Role.ADMIN
        self.assertTrue(self.user.is_admin())

    def test_str_representation(self):
        """Ensure __str__ returns 'FirstName LastName (role)'."""
        self.user.first_name = 'John'
        self.user.last_name = 'Doe'
        self.user.save()
        self.assertEqual(str(self.user), 'John Doe (customer)')
