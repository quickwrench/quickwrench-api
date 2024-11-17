from typing import Iterable

from django.contrib.auth.forms import UserChangeForm, UserCreationForm

from .models import Account


class AccountCreationForm(UserCreationForm):
    class Meta:
        model: type = Account
        fields: Iterable[str] = (
            "username",
            "email",
            "first_name",
            "last_name",
            "account_type",
        )


class AccountChangeForm(UserChangeForm):
    class Meta:
        model: type = Account
        fields: Iterable[str] = (
            "username",
            "email",
            "first_name",
            "last_name",
            "account_type",
        )
