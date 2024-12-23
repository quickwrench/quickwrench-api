import pytest
from django.core.management import call_command
from rest_framework.test import APIClient
from rest_framework_simplejwt.tokens import AccessToken
from typing import Any
from quickwrench_api.apps.accounts.models import Account
from quickwrench_api.apps.workshops.models import Service, Category


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
        phone_number="+201101234567",
    )
    return account


@pytest.fixture
def test_account() -> dict[str, Any]:
    return {
        "id": 1,
        "email": "test@test.com",
        "username": "testuser",
        "password": "testpass",
        "phone_number": "+201201234567",
<<<<<<< HEAD
=======

>>>>>>> 29eb026232c4fe274c7afb7b5c9205c0cfc9d643
    }


@pytest.fixture()
def jwt_token(authenticated_account) -> str:
    token = AccessToken.for_user(authenticated_account)
    return str(token)


@pytest.fixture
def test_service(db, load_data) -> Service:
    category: Category = Category.objects.get(id=1)
    return Service.objects.create(
        category=category,
        name="Oil",
        description="description",
        price=99,
    )
