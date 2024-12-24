from typing import Any

from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin,
)
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

from .validators import EGYPT_PHONE_REGEX


class AccountManager(BaseUserManager):
    def create_user(self, email: str, password: str, **extra_fields: Any):
        if not email:
            raise ValueError("The email field must be set")
        if not extra_fields.get("username"):
            raise ValueError("The username field must be set")

        email = self.normalize_email(email)
        extra_fields.setdefault("is_active", True)
        account = self.model(email=email, **extra_fields)
        account.set_password(password)
        account.save(using=self._db)
        return account

    def create_superuser(self, email: str, password: str, **extra_fields: Any):
        if not email:
            raise ValueError("The email field must be set")
        if not extra_fields.get("username"):
            raise ValueError("The username field must be set")

        email = self.normalize_email(email)
        extra_fields.setdefault("is_active", True)
        extra_fields.setdefault("is_superuser", True)
        account = self.model(email=email, **extra_fields)
        account.set_password(password)
        account.save(using=self._db)
        return account


class Account(AbstractBaseUser, PermissionsMixin):

    class Meta:
        verbose_name = "account"
        verbose_name_plural = "accounts"

    email: models.EmailField = models.EmailField(
        unique=True,
    )
    username: models.CharField = models.CharField(
        max_length=100,
        unique=True,
    )
    phone_number: models.CharField = models.CharField(
        max_length=13,
        unique=True,
        null=False,
        blank=False,
        default="+201101234567",
        validators=[EGYPT_PHONE_REGEX],
    )
    date_joined: models.DateField = models.DateField(
        auto_now_add=True,
    )
    is_active: models.BooleanField = models.BooleanField(
        default=True,
    )
    rating: models.FloatField = models.FloatField(
        null=False,
        blank=False,
        default=0.0,
        validators=[MinValueValidator(0), MaxValueValidator(5)],
    )

    objects = AccountManager()

    EMAIL_FIELD = "email"
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username"]

    def __str__(self) -> str:
        return self.username
