from django.db import models
from django.utils import timezone
from django.contrib.auth.models import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.contrib.auth.models import BaseUserManager
from try_django import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token

from django.contrib.auth.tokens import PasswordResetTokenGenerator
#from django.utils import six
from six import text_type

COUNTRY_CHOICES = (
    ("ALL COUNTRIES", "All Countries"),
    ("BRUNEI", "Brunei"),
    ("CAMBODIA", "Cambodia"),
    ("HONG KONG", "Hong Kong"),
    ("INDONESIA", "Indonesia"),
    ("LAOS", "Laos"),
    ("MALAYSIA", "Malaysia"),
    ("MONGOLIA", "Mongolia"),
    ("MYANMAR", "Myanmar"),
    ("PAKISTAN", "Pakistan"),
    ("PHILIPPINES", "Philippines"),
    ("SINGAPORE", "Singapore"),
    ("THAILAND", "Thailand"),
    ("VIETNAM", "Vietnam"),
)

class MemberManager(BaseUserManager):
    """Manager for member profiles"""

    def create_user(self, username, first_name, last_name, password=None):
        """Create a new user profile"""
        if not username:
            raise ValueError('User must have an email address')

        if not first_name:
            raise ValueError('Please provide your first name')

        if not last_name:
            raise ValueError('Please provide your last name')

        username = self.normalize_email(username)
        user = self.model(username=username, first_name=first_name, last_name=last_name)

        user.set_password(password)
        user.save(using=self.db)

        return user

    def create_superuser(self, username, first_name, last_name, password):
        """Create and save a new superuser with given details"""
        user = self.create_user(username, first_name, last_name, password)

        user.is_superuser = True
        user.is_staff = True
        user.is_active = True
        user.save(using=self._db)

        return user

DEPARTMENT_CHOICES = (
    ("Sales", "SALES"),
    ("Business Development", "BUSINESS DEVELOPMENT"),
    ("Marketing", "MARKETING"),
    ("Technical Support", "TECHNICAL SUPPORT"),
    ("Research & Development", "RESEARCH & DEVELOPMENT"),
    ("Finance", "FINANCE"),
    ("Legal", "LEGAL"),
)

class Member(AbstractBaseUser, PermissionsMixin):
    username = models.EmailField(max_length=100, unique=True)
    first_name = models.CharField(max_length=100, blank=True)
    last_name = models.CharField(max_length=100, blank=True)
    position = models.CharField(max_length=100, blank=True)
    department = models.CharField(max_length=50, choices=DEPARTMENT_CHOICES, default="Sales")
    photo = models.ImageField(upload_to='members/photos/%Y/%m/%d/', default="members/default/pic1.png")
    company = models.CharField(max_length=100, blank=True)
    join_date = models.DateTimeField(default=timezone.now, blank=True)
    is_staff = models.BooleanField(default=False)
    is_approved = models.BooleanField(default=True)
    is_activated = models.BooleanField(default=False)
    objects = MemberManager()

    brochure_country = models.CharField(max_length=50, choices=COUNTRY_CHOICES, default="ALL COUNTRIES")
    certificate_country = models.CharField(max_length=50, choices=COUNTRY_CHOICES, default="ALL COUNTRIES")
    eproof_country = models.CharField(max_length=50, choices=COUNTRY_CHOICES, default="ALL COUNTRIES")
    manual_country = models.CharField(max_length=50, choices=COUNTRY_CHOICES, default="ALL COUNTRIES")
    proposal_country = models.CharField(max_length=50, choices=COUNTRY_CHOICES, default="ALL COUNTRIES")
    powerpoint_country = models.CharField(max_length=50, choices=COUNTRY_CHOICES, default="ALL COUNTRIES")
    quotation_country = models.CharField(max_length=50, choices=COUNTRY_CHOICES, default="ALL COUNTRIES")
    items_per_page = models.IntegerField(default=3)


    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['first_name', 'last_name']

    def get_full_name(self):
        fullname = self.first_name+'_'+ self.last_name
        return fullname

    def get_username(self):
        return self.username

    def get_email(self):
        return self.username

    def get_short_name(self):
        return self.first_name

    def get_initials(self):
        return self.first_name[0:1] + self.last_name[0:1]

    def __str__(self):
        return self.username

class ProfileFeedItem(models.Model):
    user_profile = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )
    status_text = models.CharField(max_length=255)
    created_on = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.status_text

@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)



class TokenGenerator(PasswordResetTokenGenerator):
    def _make_hash_value(self, user, timestamp):
        return (
            text_type(user.pk) + text_type(timestamp) +
            text_type(user.is_active)
        )

account_activation_token = TokenGenerator()