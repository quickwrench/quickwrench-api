import pytest
from rest_framework.response import Response
from rest_framework.test import APIClient
from rest_framework import status
from quickwrench_api.apps.accounts.models import Account


class TestLoginView:
    def test_invalid_login_should_return_400(self, ac: APIClient):
        response: Response = ac.post("/accounts/login/")
        assert response.status_code == 400

    @pytest.mark.django_db
    def test_valid_login_returns_200(self, ac: APIClient, test_user: dict[str, str]):
        Account.objects.create_user(
            username=test_user["username"], password=test_user["password"]
        )
        response: Response = ac.post(
            "/accounts/login/",
            {"username": test_user["username"], "password": test_user["password"]},
            format="json",
        )
        assert response.status_code == 200

    @pytest.mark.django_db
    def test_valid_login_returns_tokens(self, ac: APIClient, test_user: dict[str, str]):
        Account.objects.create_user(
            username=test_user["username"], password=test_user["password"]
        )

        response: Response = ac.post(
            "/accounts/login/",
            {"username": test_user["username"], "password": test_user["password"]},
            format="json",
        )

        assert "access" in response.data
        assert "refresh" in response.data


class TestRegister:
    @pytest.mark.django_db
    def test_register_success_201(self, ac, user_data):
        response = ac.post("/accounts/register/", user_data, format="json")
        assert response.status_code == status.HTTP_201_CREATED
        assert response.data["username"] == user_data["username"]
        assert response.data["email"] == user_data["email"]

    @pytest.mark.django_db
    def test_register_with_existing_email(
        self, ac, user_data, user_with_existing_email
    ):
        user_data["email"] = user_with_existing_email.email
        response = ac.post("/accounts/register/", user_data, format="json")
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert "email" in response.data
        assert response.data["email"] == ["An account with this email already exists."]
