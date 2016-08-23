from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.contrib.auth.models import BaseUserManager
from django.core.validators import RegexValidator
from django.db import models

from django.utils import timezone

class UserManager(BaseUserManager):
    """
    Creating UserManager class from BaseUserManager
    (overridding create_user and create_superuser)
    so that users can be created using email instead of
    user_name.
    """

    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('The given email address must be set')

        now = timezone.now()
        email = UserManager.normalize_email(email)
        user = self.model(email=email,
                          is_staff=False, is_active=True, is_superuser=False,
                          last_login=now, date_joined=now, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password, **extra_fields):
        superuser = self.create_user(email, password, **extra_fields)
        superuser.is_staff = True
        superuser.is_active = True
        superuser.is_superuser = True
        superuser.is_email_verified = True
        superuser.role = "Super User"
        superuser.save(using=self._db)
        return superuser


class BaseUser(AbstractBaseUser, PermissionsMixin):
    """
    Creating custom user models using AbstractBaseUser.
    Adding custom fields (phone number) to the base user model.
    Implementing Validation on phone number.
    """
    email = models.EmailField(unique=True)

    phone_number = models.CharField(max_length=15,
                                    null=True, blank=True)
    
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)
    is_email_verified = models.BooleanField(default=False)
    date_joined = models.DateTimeField(
        auto_now_add=True,
        null=False,
        editable=True,
    )
    

    USERNAME_FIELD = 'email'

    objects = UserManager()

    # Returns short name of user.
    def get_short_name(self):
        return self.get_short_name

    def get_email(self):
        return self.get_email

    def get_date_joined(self):
        if self.date_joined:
            return str(self.date_joined)
        else:
            return str("-")

    def phone_number(self):
        if self.phone_number:
            return str(self.phone_number)
        else:
            return str("-")
            
    def is_email_verified(self):
        if self.is_email_verified:
            return str(self.is_email_verified)
        else:
            return str("False")                

class Customer(BaseUser):
    first_name = models.CharField(max_length=80, blank=True, null=True)
    last_name = models.CharField(max_length=80, blank=True, null=True)
    full_name = models.CharField(max_length=80, blank=True, null=True)
    date_of_birth = models.DateTimeField()
    address = models.TextField()



    def __unicode__(self):
        return self.full_name   


