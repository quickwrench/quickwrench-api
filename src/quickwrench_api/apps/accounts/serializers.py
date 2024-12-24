from typing import Iterable, Mapping, Optional

from rest_framework import serializers

from ..users.models import User
from ..workshops.models import Workshop
from . import utils
from .models import Account


class AccountSerializer(serializers.ModelSerializer):
    type: serializers.SerializerMethodField = serializers.SerializerMethodField()

    class Meta:
        model: type = Account
        fields: Iterable[str] = (
            "id",
            "email",
            "username",
            "password",
            "phone_number",
            "type",
        )
        extra_kwargs: Mapping[str, Mapping] = {
            "password": {"write_only": True},
        }

    def get_type(self, obj: Account) -> str:
        account_type: Optional[type[User | Workshop]] = utils.account_type(obj)
        if not account_type:
            raise serializers.ValidationError("account does not belong to any type.")
        return "workshop" if account_type is Workshop else "user"

    def create(self, validated_data: Mapping[str, str]) -> Account:
        account: Account = Account.objects.create_user(
            email=validated_data["email"],
            password=validated_data["password"],
            username=validated_data["username"],
            phone_number=validated_data["phone_number"],
        )
        return account
