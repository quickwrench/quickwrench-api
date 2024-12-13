from typing import Iterable

from rest_framework import serializers

from ..accounts.serializers import AccountSerializer
from .models import Account, Category, Workshop, Service


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields: Iterable[str] = (
            "name",
            "description",
        )


class ServiceSerializer(serializers.ModelSerializer):
    category = serializers.PrimaryKeyRelatedField(queryset=Category.objects.all())

    class Meta:
        model = Service
        fields: Iterable[str] = (
            "category",
            "name",
            "description",
            "price",
        )


class WorkshopSerializer(serializers.ModelSerializer):
    account: AccountSerializer = AccountSerializer()
    services: serializers.PrimaryKeyRelatedField = serializers.PrimaryKeyRelatedField(
        queryset=Service.objects.all(),
        many=True,
    )

    class Meta:
        model = Workshop
        fields: Iterable[str] = (
            "account",
            "address",
            "services",
        )

    def create(self, validated_data: dict) -> Workshop:
        account_data: dict[str, str] = validated_data.pop("account")
        services = validated_data.pop("services")
        account: Account = Account.objects.create_user(**account_data)
        validated_data["account"] = account
        workshop: Workshop = Workshop.objects.create(**validated_data)
        workshop.services.set(services)
        return workshop
