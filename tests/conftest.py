import pytest
from rest_framework.test import APIClient

from quickwrench_api.apps.accounts.models import Account
from quickwrench_api.apps.users.models import User
from quickwrench_api.apps.workshops.models import Category, Service, Workshop


@pytest.fixture()
def client() -> APIClient:
    return APIClient()


@pytest.fixture
def test_account() -> dict[str, str]:
    return {"email": "test@test.com", "username": "testuser", "password": "testpass"}


@pytest.fixture
def user_data(test_account):
    return {
        "account": test_account,
        "first_name": "John",
        "last_name": "Doe",
        "car_make": "BMW",
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
        "car_make": "BMW",
    }


@pytest.fixture
def user_with_existing_email(db, existing_user):
    # Create Account first
    account = Account.objects.create_user(
        email=existing_user["account"]["email"],
        username=existing_user["account"]["username"],
        password=existing_user["account"]["password"],
    )
    # Create User and link to Account explicitly
    user = User.objects.create(
        account=account,
        first_name=existing_user["first_name"],
        last_name=existing_user["last_name"],
        car_make=existing_user["car_make"],
    )
    return user


# category
@pytest.fixture
def test_category():
    return Category.objects.create(name="Testcategroy", description="testdescription")


# service
@pytest.fixture
def test_service(test_category):
    return Service.objects.create(
        category=test_category,
        name="Oil",
        description="description",
        price=99,
    )


# workshops
@pytest.fixture
def workshops_valid_data(test_account, test_service):
    return {
        "account": test_account,
        "services": [test_service.id],
        "address": "zayed",
    }


@pytest.fixture
def workshop_with_existing_email(db, test_service):

    account = Account.objects.create(
        email="existingworkshop@example.com",
        username="existingworkshop",
        password="workshoppass",
    )

    workshop = Workshop.objects.create(
        account=account,
        address="zayed",
    )
    workshop.services.set([test_service])

    return workshop
