from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

from ..accounts.models import Account
from ..carmakes.models import CarMake


class Category(models.Model):
    name: models.CharField = models.CharField(
        max_length=50,
        blank=False,
        null=False,
        unique=True,
    )
    description: models.TextField = models.TextField(
        blank=True,
        null=True,
    )

    def __str__(self) -> str:
        return self.name


class Service(models.Model):
    category: models.ForeignKey = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        related_name="services",
    )
    name: models.CharField = models.CharField(
        max_length=100,
        null=False,
        blank=False,
    )
    description: models.TextField = models.TextField(
        null=True,
        blank=True,
    )
    price: models.PositiveBigIntegerField = models.PositiveBigIntegerField(
        null=False,
        blank=False,
        validators=[MinValueValidator(0), MaxValueValidator(999999)],
    )

    def __str__(self) -> str:
        return self.name


class Workshop(models.Model):
    name: models.CharField = models.CharField(
        max_length=200,
        null=False,
        blank=False,
    )
    carmakes: models.ManyToManyField = models.ManyToManyField(
        CarMake,
        blank=False,
    )
    account: models.OneToOneField = models.OneToOneField(
        Account,
        on_delete=models.CASCADE,
    )
    services: models.ManyToManyField = models.ManyToManyField(
        Service,
        related_name="workshops",
        blank=False,
    )
    address: models.CharField = models.CharField(
        max_length=200,
        null=False,
        blank=False,
    )

    def __str__(self) -> str:
        return self.name
