from __future__ import unicode_literals

import os

from django.conf import settings
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.core.urlresolvers import reverse
from django.db import models
from django.template.loader import render_to_string
from django.utils.translation import ugettext_lazy as _

from .signals import create_auth_token

class AccountManager(BaseUserManager):
    """ Manager class that contains methods for
        the account model
    """
    def create_user(self, email, password=None, **kwargs):
        """ create user account
        """
        if not email:
            raise ValueError("Email is required")

        # create account
        email = self.normalize_email(email)
        account = self.model(email=email, username=email)
        account.set_password(password)
        account.save()

        return account

    def create_superuser(self, email, password, **kwargs):
        """ creates a user that has administrative
            access. (can access the admin panel)
        """
        account = self.create_user(email, password, **kwargs)
        account.is_admin = True
        account.is_staff = True
        account.is_superuser = True
        account.save()

        return account

def profile_photo_location(instance, filename):
    return "account/photos/%s/%s" %(instance.id, filename)

class Account(AbstractBaseUser, PermissionsMixin):
    """ Custom model for the account user. it is
        an override from the `django.auth.models.User`
    """
    MALE = "m"
    FEMALE = "f"
    GENDER = (
        (MALE, "Male"),
        (FEMALE, "Female"),
    )

    MANAGEMENT = "management"
    DEVELOPER = "developer"
    DESIGNER = "designer"
    POSITION = (
        (MANAGEMENT, "Management"),
        (DEVELOPER, "Software Developer"),
        (DESIGNER, "UI/UX Designer"),
    )

    email = models.EmailField(max_length=225, unique=True)
    username = models.CharField(max_length=225, unique=True)
    first_name = models.CharField(max_length=50, blank=True, null=True)
    last_name = models.CharField(max_length=50, blank=True, null=True)
    birthdate = models.DateField(blank=True, null=True)
    gender = models.CharField(max_length=1, choices=GENDER, default=MALE)
    contact = models.CharField(max_length=11, null=True, blank=True)
    address = models.TextField(null=True, blank=True)
    position = models.CharField(max_length=35, choices=POSITION, default=DEVELOPER)
    job_title = models.CharField(max_length=100, null=True, blank=True)
    employment_startdate = models.DateField(blank=True, null=True)
    profile_photo = models.ImageField(upload_to=profile_photo_location, blank=True, null=True)

    date_joined = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    is_admin = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(_('active'), default=True,
        help_text=_('Designates whether this user should be treated as '
                    'active. Unselect this instead of deleting accounts.'))

    objects = AccountManager()
    
    USERNAME_FIELD = 'email'

    def get_full_name(self):
        """ returns the user's full name
        """
        return "{first_name} {last_name}".format(
            first_name=self.first_name,
            last_name=self.last_name
            )

    def get_short_name(self):
        return self.first_name