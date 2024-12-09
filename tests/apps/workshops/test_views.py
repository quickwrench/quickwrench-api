import pytest
from rest_framework import status
from rest_framework.response import Response

from rest_framework.test import APIClient


class TestWorkshop:
    @pytest.mark.django_db
    def test_workshop_success_201(self, client: APIClient, workshops_valid_data):
        response: Response = client.post(
            "/workshops/register/", workshops_valid_data, format="json"
        )
        assert response.status_code == status.HTTP_201_CREATED
        assert (
            response.data["account"]["username"]
            == workshops_valid_data["account"]["username"]
        )
        assert (
            response.data["account"]["email"]
            == workshops_valid_data["account"]["email"]
        )
        assert response.data["address"] == workshops_valid_data["address"]
        assert set(response.data["services"]) == set(workshops_valid_data["services"])

    @pytest.mark.django_db
    def test_workshop_with_existing_email(
        self,
        client: APIClient,
        workshop_with_existing_email,
        test_service,
    ):
        payload = {
            "account": {
                "email": workshop_with_existing_email.account.email,
                "username": "newuser",
                "password": "newpassword",
            },
            "address": "zayed",
            "service": [test_service.id],
        }

        response: Response = client.post("/workshops/register/", payload, format="json")

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert "email" in response.data["account"]
        assert response.data["account"]["email"] == [
            "account with this email already exists."
        ]

    @pytest.mark.django_db
    @pytest.mark.parametrize(
        "email, expected_error",
        [
            ("plainaddress", "Enter a valid email address."),
            ("@missingusername.com", "Enter a valid email address."),
            ("username@.com", "Enter a valid email address."),
            ("username@domain", "Enter a valid email address."),
            ("username@domain,com", "Enter a valid email address."),
            ("username@domain..com", "Enter a valid email address."),
            ("", "This field may not be blank."),
            (None, "This field may not be null."),
        ],
    )
    def test_workshops_with_invalid_email(
        self, client: APIClient, workshops_valid_data, email, expected_error
    ):
        workshops_valid_data["account"]["email"] = email
        response = client.post(
            "/workshops/register/", workshops_valid_data, format="json"
        )
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response.data["account"]["email"] == [expected_error]

    @pytest.mark.django_db
    def test_workshop_missing_username(self, client: APIClient, workshops_valid_data):
        workshops_valid_data["account"]["username"] = ""
        response: Response = client.post(
            "/workshops/register/", workshops_valid_data, format="json"
        )
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert "username" in response.data["account"]
        assert response.data["account"]["username"] == ["This field may not be blank."]

    @pytest.mark.django_db
    def test_workshop_missing_password(self, client: APIClient, workshops_valid_data):
        workshops_valid_data["account"]["password"] = ""
        response: Response = client.post(
            "/workshops/register/", workshops_valid_data, format="json"
        )
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert "password" in response.data["account"]
        assert response.data["account"]["password"] == ["This field may not be blank."]
