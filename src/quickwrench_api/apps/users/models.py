from django.db import models

from ..accounts.models import Account


class CarMake(models.TextChoices):
    BMW = "BMW", "BMW"
    AUDI = "AUDI", "Audi"
    TOYOTA = "TOYOTA", "Toyota"
    HONDA = "HONDA", "Honda"
    FORD = "FORD", "Ford"


class User(models.Model):
    account: models.OneToOneField = models.OneToOneField(
        Account, on_delete=models.CASCADE
    )
    first_name: models.CharField = models.CharField(
        max_length=200, null=False, blank=False
    )
    last_name: models.CharField = models.CharField(
        max_length=200, null=False, blank=False
    )
    car_make: models.CharField = models.CharField(
        max_length=50, choices=CarMake, null=True
    )
