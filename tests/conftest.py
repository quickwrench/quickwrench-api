import pytest
from rest_framework.test import APIClient
from django.core.management import call_command
from quickwrench_api.apps.accounts.models import Account
from quickwrench_api.apps.users.models import User
from quickwrench_api.apps.car_makes.models import CarMake
from rest_framework_simplejwt.tokens import AccessToken


@pytest.fixture()
def client() -> APIClient:
    return APIClient()


@pytest.fixture(scope="function")
def load_data(db, django_db_blocker):
    with django_db_blocker.unblock():
        call_command("loaddata", "carmakes.json")


@pytest.fixture()
def authenticated_account(db) -> Account:
    account = Account.objects.create_user(
        username="authenticated_user",
        email="authenticated@test.com",
        password="testpass",
    )
    return account


@pytest.fixture()
def jwt_token(authenticated_account) -> str:
    token = AccessToken.for_user(authenticated_account)
    return str(token)


@pytest.fixture
def test_account() -> dict[str, str]:
    return {"email": "test@test.com", "username": "testuser", "password": "testpass"}


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
