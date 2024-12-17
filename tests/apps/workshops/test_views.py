import pytest

from rest_framework import status
from rest_framework.response import Response
from rest_framework.test import APIClient


class TestWorkshop:

    @pytest.mark.django_db
    def test_category_returns_instance_200(self, client, load_data):
        response: Response = client.get("/workshops/categories/")
        data = response.json()
        instance_count = len(data)
        print(data)
        assert response.status_code == status.HTTP_200_OK
        assert instance_count == 9

    @pytest.mark.django_db
    def test_workshop_success_201(self, client: APIClient, workshop_data):
        response: Response = client.post(
            "/workshops/register/", workshop_data, format="json"
        )
        assert response.status_code == status.HTTP_201_CREATED

    @pytest.mark.django_db
    def test_workshop_register_expected_response(
        self, client: APIClient, workshop_data
    ):
        response: Response = client.post(
            "/workshops/register/", workshop_data, format="json"
        )
        expected_data = workshop_data
        expected_data["account"].pop("password")
        assert response.json() == expected_data

    @pytest.mark.django_db
    def test_workshop_with_existing_email(
        self,
        client: APIClient,
        workshop_with_existing_email,
    ):
        payload = {
            "carmakes": [1],
            "account": {
                "email": workshop_with_existing_email.account.email,
                "username": "newuser",
                "password": "newpassword",
            },
            "address": "zayed",
            "services": [
                {
                    "category": 1,
                    "name": "Oil",
                    "description": "change oil",
                    "price": 1000,
                }
            ],
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
        self, client: APIClient, workshop_data, email: str, expected_error: str
    ):
        workshop_data["account"]["email"] = email
        response: Response = client.post(
            "/workshops/register/", workshop_data, format="json"
        )
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response.data["account"]["email"] == [expected_error]

    @pytest.mark.django_db
    def test_workshop_missing_username(self, client: APIClient, workshop_data):
        workshop_data["account"]["username"] = ""
        response: Response = client.post(
            "/workshops/register/", workshop_data, format="json"
        )
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert "username" in response.data["account"]
        assert response.data["account"]["username"] == ["This field may not be blank."]

    @pytest.mark.django_db
    def test_workshop_missing_password(self, client: APIClient, workshop_data):
        workshop_data["account"]["password"] = ""
        response: Response = client.post(
            "/workshops/register/", workshop_data, format="json"
        )
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert "password" in response.data["account"]
        assert response.data["account"]["password"] == ["This field may not be blank."]
