"""Tests for the UserRegistrationForm."""
from django.test import TestCase
from django.contrib.auth import get_user_model
from users.forms import UserRegistrationForm
from users.models import Customer

User = get_user_model()

class UserRegistrationFormTestCase(TestCase):
    """Tests for the UserRegistrationForm."""

    def setUp(self):
        """Prepare valid form data you can reuse in multiple tests."""
        self.valid_form_data = {
            'username': 'testuser',
            'email': 'test@example.com',
            'first_name': 'Test',
            'last_name': 'User',
            'password1': 'TestPass123',
            'password2': 'TestPass123',
        }

    def test_form_is_valid_with_proper_data(self):
        """Test if form is valid when all required fields are provided and passwords match."""
        form = UserRegistrationForm(data=self.valid_form_data)
        self.assertTrue(form.is_valid())
        user = form.save()  

        # Check User model data
        self.assertEqual(user.username, 'testuser')
        self.assertEqual(user.email, 'test@example.com')
        self.assertEqual(user.first_name, 'Test')
        self.assertEqual(user.last_name, 'User')
        self.assertEqual(user.role, User.Role.CUSTOMER) 

        # Verify a corresponding Customer object is created
        customer = Customer.objects.filter(user=user).first()
        self.assertIsNotNone(customer, "A Customer object should be created for the user.")

    def test_form_is_invalid_when_email_is_missing(self):
        """Test if form invalid if the email is missing."""
        invalid_data = self.valid_form_data.copy()
        del invalid_data['email'] 

        form = UserRegistrationForm(data=invalid_data)
        self.assertFalse(form.is_valid())
        self.assertIn('email', form.errors)

    def test_form_is_invalid_when_username_is_blank(self):
        """Test if form invalid if the username is blank."""
        invalid_data = self.valid_form_data.copy()
        invalid_data['username'] = ''

        form = UserRegistrationForm(data=invalid_data)
        self.assertFalse(form.is_valid())
        self.assertIn('username', form.errors)

    def test_form_fails_password_mismatch(self):
        """Test if form invalid if passwords do not match."""
        invalid_data = self.valid_form_data.copy()
        invalid_data['password2'] = 'DifferentPass123'

        form = UserRegistrationForm(data=invalid_data)
        self.assertFalse(form.is_valid())
        self.assertIn('password2', form.errors)

    def test_form_save_creates_customer_when_commit_true(self):
        """Test if form saves creates a customer user."""
        form = UserRegistrationForm(data=self.valid_form_data)
        self.assertTrue(form.is_valid())

        # Save with commit=True
        user = form.save(commit=True)
        # Customer object should exist
        customer_exists = Customer.objects.filter(user=user).exists()
        self.assertTrue(customer_exists)

    def test_form_save_does_not_create_customer_if_commit_false(self):
        """Test if form doesn't create user when invalid."""
        form = UserRegistrationForm(data=self.valid_form_data)
        self.assertTrue(form.is_valid())

        user = form.save(commit=False)
        self.assertEqual(Customer.objects.count(), 0)
        user.save()
        customer_exists = Customer.objects.filter(user=user).exists()
        self.assertFalse(customer_exists, "No Customer is created if commit=False was used.")