import pytest
from rest_framework.response import Response
from rest_framework.test import APIClient

from quickwrench_api.apps.accounts.models import Account


class TestLoginView:
    def test_invalid_login_should_return_400(self, client: APIClient):
        response: Response = client.post("/accounts/login/")
        assert response.status_code == 400

    @pytest.mark.django_db
    def test_valid_login_returns_200(
        self, client: APIClient, test_account: dict[str, str]
    ):
        Account.objects.create_user(**test_account)

        response: Response = client.post(
            "/accounts/login/", test_account, format="json"
        )

        assert response.status_code == 200

    @pytest.mark.django_db
    def test_valid_login_returns_tokens(
        self, client: APIClient, test_account: dict[str, str]
    ):
        Account.objects.create_user(**test_account)

        response: Response = client.post(
            "/accounts/login/", test_account, format="json"
        )

        assert "access" in response.data
        assert "refresh" in response.data
