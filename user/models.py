from django.db import models
from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager


# Manager for the Account class
class AccountManager(BaseUserManager):

    def create_user(self, email, username, password=None):
        if not email:
            raise ValueError('Please provide an email!')

        user = self.model(
            email=self.normalize_email(email),
            username=username,
        )

        user.set_password(password)
        user.save(using=self.db)
        return user


# Model for the account table
class Account(AbstractBaseUser):

    email = models.EmailField(max_length=60, unique=True, verbose_name='Email Address')
    username = models.CharField(max_length=30, unique=True)
    objects = AccountManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    def __str__(self):
        return self.email