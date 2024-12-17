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
    )
    user = User.objects.create(
        account=account,
        first_name=existing_user["first_name"],
        last_name=existing_user["last_name"],
        car_make=car_make,
    )
    return user


@pytest.fixture()
def user_to_fetch(db, load_data) -> User:
    car_make: CarMake = CarMake.objects.get(id=1)
    account: Account = Account.objects.create_user(
        email="testuser@test.com", username="username123", password="testpass"
    )
    user: User = User.objects.create(
        account=account, first_name="first", last_name="last", car_make=car_make
    )
    return user
