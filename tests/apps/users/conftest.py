import pytest

from quickwrench_api.apps.accounts.models import Account
from quickwrench_api.apps.car_makes.models import CarMake
from quickwrench_api.apps.users.models import User


@pytest.fixture
def user_data(test_account):
    return {
        "account": test_account,
        "first_name": "John",
        "last_name": "Doe",
        "car_make": 1,
    }


@pytest.fixture
def existing_user():
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
def user_with_existing_email(db, existing_user, load_data):
    car_make = CarMake.objects.get(id=1)
    account = Account.objects.create_user(
        email=existing_user["account"]["email"],
        username=existing_user["account"]["username"],
        password=existing_user["account"]["password"],
        phone_number=existing_user["account"]["phone_number"],
    )
    user = User.objects.create(
        account=account,
        first_name=existing_user["first_name"],
        last_name=existing_user["last_name"],
        car_make=car_make,
    )
    return user
