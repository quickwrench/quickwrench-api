from typing import Iterable, Mapping

from rest_framework import serializers

from .models import Account


class AccountSerializer(serializers.ModelSerializer):
    class Meta:
        model: type = Account
        fields: Iterable[str] = ("id", "email", "username", "password")
        extra_kwargs: Mapping[str, Mapping] = {
            "password": {"write_only": True},
        }

    def create(self, validated_data: Mapping[str, str]) -> Account:
        account: Account = Account.objects.create_user(
            email=validated_data["email"],
            password=validated_data["password"],
            username=validated_data["username"],
        )
        return account
