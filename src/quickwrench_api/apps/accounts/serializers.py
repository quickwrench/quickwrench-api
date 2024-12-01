from rest_framework import serializers
from .models import Account


class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = (
            "username",
            "email",
            "first_name",
            "last_name",
            "password",
            "account_type",
        )
        extra_kwargs = {
            "password": {"write_only": True},
        }

    def validate_email(self, value):
        if Account.objects.filter(email=value).exists():
            raise serializers.ValidationError(
                "An account with this email already exists."
            )
        return value

    def create(self, validated_data):
        password = validated_data.pop("password")
        account = Account(**validated_data)
        account.set_password(password)
        account.save()
        return account
