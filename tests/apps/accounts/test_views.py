import pytest
from rest_framework import status
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


class TestAccountDetailsView:

    def test_account_details_endpoint_for_user_returns_200(
        self, client, jwt_token, authenticated_user
    ):
        client.credentials(HTTP_AUTHORIZATION=f"Bearer {jwt_token}")
        response = client.get("/accounts/me/")
        assert response.status_code == status.HTTP_200_OK

    @pytest.mark.django_db
    def test_account_details_endpoint_for_user_returns_expected_data_and_user_type(
        self, client, jwt_token, authenticated_user
    ):
        client.credentials(HTTP_AUTHORIZATION=f"Bearer {jwt_token}")
        response = client.get("/accounts/me/")
        response_data = response.json()
        assert response_data["type"] == "user"
        assert response_data["email"] == authenticated_user.account.email
        assert response_data["username"] == authenticated_user.account.username
        assert "id" in response_data

    @pytest.mark.django_db
    def test_account_details_endpoint_for_workshop_returns_200(
        self, client, jwt_token, authenticated_workshop
    ):
        client.credentials(HTTP_AUTHORIZATION=f"Bearer {jwt_token}")
        response = client.get("/accounts/me/")
        assert response.status_code == status.HTTP_200_OK

    def test_account_details_endpoint_for_workshop_returns_expected_data_and_workshop_type(
        self, client, jwt_token, authenticated_workshop
    ):
        client.credentials(HTTP_AUTHORIZATION=f"Bearer {jwt_token}")
        response = client.get("/accounts/me/")
        response_data = response.json()
        assert response_data["type"] == "workshop"
        assert response_data["email"] == authenticated_workshop.account.email
        assert response_data["username"] == authenticated_workshop.account.username
        assert "id" in response_data

    @pytest.mark.django_db
    def test_account_details_endpoint_with_no_associated_type_returns_400(
        self, client, jwt_token
    ):
        client.credentials(HTTP_AUTHORIZATION=f"Bearer {jwt_token}")
        response = client.get("/accounts/me/")
        assert response.status_code == status.HTTP_400_BAD_REQUEST

    @pytest.mark.django_db
    def test_account_details_endpoint_with_no_associated_type_returns_expected_message(
        self, client, jwt_token
    ):
        client.credentials(HTTP_AUTHORIZATION=f"Bearer {jwt_token}")
        response = client.get("/accounts/me/")
        response_data = response.json()

        assert response_data["message"] == "no associated user or workshop found"
