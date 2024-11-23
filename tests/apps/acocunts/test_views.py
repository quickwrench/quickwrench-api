import pytest
from rest_framework.response import Response
from rest_framework.test import APIClient

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
