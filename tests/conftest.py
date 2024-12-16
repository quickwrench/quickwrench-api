import pytest
from django.core.management import call_command
from rest_framework.test import APIClient
from rest_framework_simplejwt.tokens import AccessToken

from quickwrench_api.apps.accounts.models import Account
from quickwrench_api.apps.car_makes.models import CarMake
from quickwrench_api.apps.users.models import User
from quickwrench_api.apps.workshops.models import Category, Service, Workshop


@pytest.fixture()
def client() -> APIClient:
    return APIClient()


@pytest.fixture(autouse=True, scope="function")
def load_data(db, django_db_blocker):
    with django_db_blocker.unblock():
        call_command("loaddata", "carmakes.json")
        call_command("loaddata", "categories.json")


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


# # category
# @pytest.fixture
# def test_category():
#     return Category.objects.create(name="Testcategroy", description="testdescription")


# service
@pytest.fixture
def test_service(db, load_data):
    category = Category.objects.get(id=1)
    return Service.objects.create(
        category=category,
        name="Oil",
        description="description",
        price=99,
    )


@pytest.fixture
def workshop_data(test_account, test_service):
    return {
        # "carmakes": [{"id": 1}],
        "account": test_account,
        "carmakes": [1],  # Pass only the IDs of the car makes, not a dictionary
        "services": [
            {
                "name": test_service.name,
                "description": test_service.description,
                "category": test_service.category.id,  # Assuming category is passed as ID
                "price": test_service.price,
            }
        ],
        "address": "zayed",
    }


@pytest.fixture
def existing_workshop():
    return {
        "account": {
            "email": "existinguser@example.com",
            "username": "existinguser",
            "password": "testpass",
        },
        "address": "zayed",
    }


@pytest.fixture
def workshop_with_existing_email(db, test_service, existing_workshop, load_data):
    carmakes = CarMake.objects.get(id=1)
    account = Account.objects.create(
        email=existing_workshop["account"]["email"],
        username=existing_workshop["account"]["username"],
        password=existing_workshop["account"]["password"],
    )
    workshop = Workshop.objects.create(
        account=account,
        address=existing_workshop["address"],
    )
    workshop.services.set([test_service])
    workshop.carmakes.set([carmakes])
    return workshop
