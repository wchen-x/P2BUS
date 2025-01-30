# users/tests/test_views.py

from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from django.contrib.messages import get_messages
from django.contrib.auth import get_user_model
from users.forms import UserRegistrationForm

User = get_user_model()

class RegisterViewTestCase(TestCase):
    """Tests for the register view."""

    def setUp(self):
        self.url = reverse("register")

    def test_register_view_get(self):
        """Test GET in register view."""
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "users/register.html")
        self.assertIn("form", response.context)
        self.assertIsInstance(response.context["form"], UserRegistrationForm)

    def test_register_view_post_valid_data(self):
        """Test POST in register view."""
        form_data = {
            "username": "testuser",
            "email": "test@example.com",
            "password1": "TestPass123",
            "password2": "TestPass123",
            "first_name": "Test",
            "last_name": "User"
        }
        response = self.client.post(self.url, form_data, follow=True)

        # Check redirect to 'home'
        self.assertRedirects(response, reverse("home"))

        # Check user was created
        user_exists = User.objects.filter(username="testuser").exists()
        self.assertTrue(user_exists)

        # Check the user is logged in
        self.assertTrue(response.wsgi_request.user.is_authenticated)
        self.assertEqual(response.wsgi_request.user.username, "testuser")

        # Check success message
        messages = list(get_messages(response.wsgi_request))
        self.assertTrue(any("Registration successful!" in str(m) for m in messages))

    def test_register_view_post_invalid_data(self):
        """Test POST for invalid data in register view."""
        invalid_data = {
            "username": "testuser",
            "email": "",  # missing or blank email
            "password1": "TestPass123",
            "password2": "Mismatch123",  # password mismatch
        }
        response = self.client.post(self.url, invalid_data, follow=True)

        # The view should return status code 200 with the same template rendered
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "users/register.html")

        # The form should have errors
        form = response.context["form"]
        self.assertTrue(form.errors)

        # No user should be created
        user_exists = User.objects.filter(username="testuser").exists()
        self.assertFalse(user_exists)

        # Check error message
        messages = list(get_messages(response.wsgi_request))
        self.assertTrue(any("Registration failed" in str(m) for m in messages))
