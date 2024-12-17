from django.db import models

from ..accounts.models import Account
from quickwrench_api.apps.car_makes.models import CarMake


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
    car_make: models.ForeignKey = models.ForeignKey(
        CarMake, on_delete=models.SET_NULL, null=True, blank=True, related_name="users"
    )
