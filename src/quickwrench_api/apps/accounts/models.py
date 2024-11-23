from django.contrib.auth.models import AbstractUser
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models


class AccountType(models.TextChoices):
    USER = "USR"
    WORKSHOP = "WRK"


class Account(AbstractUser):
    class Meta:
        verbose_name = "account"
        verbose_name_plural = "accounts"

    account_type: models.CharField = models.CharField(
        null=False,
        blank=False,
        max_length=3,
        choices=AccountType,
        default=AccountType.USER,
    )
    rating: models.FloatField = models.FloatField(
        null=False,
        blank=False,
        default=0.0,
        validators=[MinValueValidator(0), MaxValueValidator(5)],
    )

    def __str__(self) -> str:
        return self.username
