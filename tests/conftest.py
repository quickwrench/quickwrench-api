import pytest
from rest_framework.test import APIClient

from quickwrench_api.apps.accounts.models import Account


@pytest.fixture()
def client() -> APIClient:
    return APIClient()


@pytest.fixture
def test_account() -> dict[str, str]:
    return {"email": "test@test.com", "username": "testuser", "password": "testpass"}


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
