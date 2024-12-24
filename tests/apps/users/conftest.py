from typing import Any

import pytest

from quickwrench_api.apps.accounts.models import Account
from quickwrench_api.apps.carmakes.models import CarMake
from quickwrench_api.apps.users.models import User


@pytest.fixture
def user_data(test_account) -> dict[str, Any]:
    return {
        "account": test_account,
        "first_name": "John",
        "last_name": "Doe",
        "carmake": 1,
    }


@pytest.fixture
def existing_user() -> dict[str, Any]:
    return {
        "account": {
            "email": "existinguser@example.com",
            "username": "existinguser",
            "password": "testpass",
            "phone_number": "+201101234567",
        },
        "first_name": "John",
        "last_name": "Doe",
    }


@pytest.fixture
def user_with_existing_email(db, existing_user, load_data) -> User:
    carmake: CarMake = CarMake.objects.get(id=1)
    account: Account = Account.objects.create_user(
        email=existing_user["account"]["email"],
        username=existing_user["account"]["username"],
        password=existing_user["account"]["password"],
        phone_number=existing_user["account"]["phone_number"],
    )
    user: User = User.objects.create(
        account=account,
        first_name=existing_user["first_name"],
        last_name=existing_user["last_name"],
        carmake=carmake,
    )
    return user


@pytest.fixture()
def user_instance(db, load_data) -> User:
    carmake: CarMake = CarMake.objects.get(id=1)
    account: Account = Account.objects.create_user(
        email="testuser@test.com", username="username123", password="testpass"
    )
    user: User = User.objects.create(
        account=account, first_name="first", last_name="last", carmake=carmake
    )
    return user
