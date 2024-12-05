from typing import Iterable

from rest_framework import serializers

from ..accounts.serializers import AccountSerializer
from .models import Account, User


class RegisterSerializer(serializers.ModelSerializer):
    account: AccountSerializer = AccountSerializer()

    class Meta:
        model: type = User
        fields: Iterable[str] = (
            "account",
            "first_name",
            "last_name",
            "car_make",
        )

    def create(self, validated_data: dict) -> User:
        account_data: dict[str, str] = validated_data.pop("account")
        account: Account = Account.objects.create_user(**account_data)
        validated_data["account"] = account
        user: User = User.objects.create(**validated_data)
        user.save()
        return user
