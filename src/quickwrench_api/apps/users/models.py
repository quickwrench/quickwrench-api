from django.db import models

from quickwrench_api.apps.carmakes.models import CarMake

from ..accounts.models import Account


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
    carmake: models.ForeignKey = models.ForeignKey(
        CarMake, on_delete=models.SET_NULL, null=True, blank=True, related_name="users"
    )
