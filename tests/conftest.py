import pytest
from django.core.management import call_command
from rest_framework.test import APIClient
from rest_framework_simplejwt.tokens import AccessToken

from quickwrench_api.apps.accounts.models import Account


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


@pytest.fixture
def test_account() -> dict[str, str]:
    return {"email": "test@test.com", "username": "testuser", "password": "testpass"}


@pytest.fixture()
def jwt_token(authenticated_account) -> str:
    token = AccessToken.for_user(authenticated_account)
    return str(token)
