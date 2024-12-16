from typing import Iterable

from rest_framework import serializers

from ..accounts.serializers import AccountSerializer
from .models import Account, Category, Workshop, Service
from ..car_makes.models import CarMake


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields: Iterable[str] = (
            "name",
            "description",
        )


class ServiceSerializer(serializers.ModelSerializer):
    category = serializers.PrimaryKeyRelatedField(
        default=1,
        queryset=Category.objects.all(),
    )
    price = serializers.IntegerField(
        default=1000,
    )

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
    carmakes: serializers.PrimaryKeyRelatedField = serializers.PrimaryKeyRelatedField(
        queryset=CarMake.objects.all(),
        many=True,
        default=1,
    )
    services: ServiceSerializer = ServiceSerializer(
        many=True,
    )

    class Meta:
        model: type = Workshop
        fields: Iterable[str] = (
            "carmakes",
            "account",
            "address",
            "services",
        )

    def create(self, validated_data: dict) -> Workshop:
        account_data: dict[str, str] = validated_data.pop("account")
        services_data = validated_data.pop("services")
        carmake_ids = validated_data.pop("carmakes")
        account: Account = Account.objects.create_user(**account_data)
        validated_data["account"] = account
        services = []
        for service_data in services_data:
            service = Service.objects.create(**service_data)
            services.append(service)
        workshop: Workshop = Workshop.objects.create(**validated_data)
        workshop.carmakes.set(carmake_ids)
        workshop.services.set(services)
        return workshop
