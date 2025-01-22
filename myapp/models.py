from django.db import models

from django.core.validators import RegexValidator
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _
from django.utils.timezone import now
from libgravatar import Gravatar
from datetime import timedelta
from django.core.exceptions import ValidationError

class Address(models.Model):
    """Model for storing user addresses"""
    
    


class User(AbstractUser):
    """Model used for user authentication, and team member related information."""

    first_name = models.CharField(max_length=50, blank=False)
    last_name = models.CharField(max_length=50, blank=False)
    email = models.EmailField(unique=True, blank=False)
    

    class UserType(models.TextChoices):
        ADMIN = "admin", _("Admin")
        TUTOR = "tutor", _("Tutor")
        STUDENT = "student", _("Student")
    role = models.CharField(max_length=7, choices=UserType, default=UserType.STUDENT)

    class Meta:
        """Model options."""

        ordering = ['last_name', 'first_name']

    def save(self, *args, **kwargs):
        new_user = not self.pk
        super().save(*args, **kwargs)
        # If new user is created
        if new_user:
            # New admin and tutor accounts have to be approved
            if self.is_admin() or self.is_tutor():
                self.is_active = False
                self.save()
            # Create tutor or student record for relevant user
            if self.is_tutor():
                Tutor.objects.create(user_id=self, fee=10)
            elif self.is_student():
                Student.objects.create(user_id=self)

    def full_name(self):
        """Return a string containing the user's full name."""

        return f'{self.first_name} {self.last_name}'

    def gravatar(self, size=120):
        """Return a URL to the user's gravatar."""

        gravatar_object = Gravatar(self.email)
        gravatar_url = gravatar_object.get_image(size=size, default='robohash')
        return gravatar_url

    def mini_gravatar(self):
        """Return a URL to a miniature version of the user's gravatar."""

        return self.gravatar(size=60)

    def is_admin(self):
        """Return whether user is admin."""

        return self.role == self.UserType.ADMIN

    def is_tutor(self):
        """Return whether user is tutor."""

        return self.role == self.UserType.TUTOR

    def is_student(self):
        """Return whether user is student."""

        return self.role == self.UserType.STUDENT

class Tutor(models.Model):
    """ Model used to store Tutor expertise, availability and their fee/hour """

    user_id = models.OneToOneField(User, on_delete = models.CASCADE, related_name = "tutor_record", primary_key = True)

    expertise = models.JSONField(default = list)                                                                                    # Stores expertise as a list of known languages
    availability = models.JSONField(default = dict)                                                                                 #  & stores availability as dictionary of days of the week (Monday, Tuesday etc.) and then a list of times available
    
    fee = models.DecimalField(max_digits = 6, decimal_places = 2, default=0.0)

    def clean(self):
        super().clean()
        if self.fee <= 0:
            raise ValidationError("Fee must be greater than 0.")

    def username(self):
        """ Return the Tutor's associated username """

        return self.user_id.username

