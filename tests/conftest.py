import pytest
from rest_framework.test import APIClient


@pytest.fixture(scope="session")
def ac() -> APIClient:
    return APIClient()


@pytest.fixture
def test_user() -> dict[str, str]:
    return {"username": "testuser", "password": "testpass"}
