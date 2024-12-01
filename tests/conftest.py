import pytest
from rest_framework.test import APIClient
from quickwrench_api.apps.accounts.models import Account


@pytest.fixture()
def ac() -> APIClient:
    return APIClient()


@pytest.fixture
def test_user() -> dict[str, str]:
    return {"username": "testuser", "password": "testpass"}


@pytest.fixture
def user_data():
    return {
        "username": "testuser",
        "email": "testuser@example.com",
        "password": "testpassword123",
        "first_name": "Test",
        "last_name": "User",
        "account_type": "USR",
    }


@pytest.fixture
def user_with_existing_email():
    user = Account.objects.create_user(
        username="existinguser",
        email="existinguser@example.com",
        password="password123",
    )
    return user
