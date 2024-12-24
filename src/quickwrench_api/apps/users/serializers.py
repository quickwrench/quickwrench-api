from typing import Iterable

from rest_framework import serializers

from ..accounts.serializers import AccountSerializer
from ..carmakes.models import CarMake
from .models import Account, User


class UserSerializer(serializers.ModelSerializer):
    account: AccountSerializer = AccountSerializer()
    carmake: serializers.PrimaryKeyRelatedField = serializers.PrimaryKeyRelatedField(
        queryset=CarMake.objects.all(),
        default=1,
    )

    class Meta:
        model: type = User
        fields: Iterable[str] = (
            "account",
            "first_name",
            "last_name",
            "carmake",
        )

    def create(self, validated_data: dict) -> User:
        account_data: dict[str, str] = validated_data.pop("account")
        account: Account = Account.objects.create_user(**account_data)
        validated_data["account"] = account
        user: User = User.objects.create(**validated_data)
        user.save()
        return user
