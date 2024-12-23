import pytest

from rest_framework import status
from rest_framework.response import Response
from rest_framework.test import APIClient
from quickwrench_api.apps.workshops.models import Workshop


class TestWorkshop:

    @pytest.mark.django_db
    def test_category_returns_instance_200(self, client: APIClient, load_data):
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
    def test_register_workshop_with_existing_email(
        self, client: APIClient, workshop_with_existing_email: Workshop
    ):

        payload = {
            "carmakes": [1],
            "account": {
                "email": workshop_with_existing_email.account.email,
                "username": "newuser",
                "password": "newpassword",
                "phone_number": "+20110124567",
            },
            "name": "bimmerfixes",
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

    @pytest.mark.django_db
    def test_filter_workshop_by_name(
        db, client: APIClient, workshop_with_existing_email: Workshop
    ):
        response: Response = client.get(
            "/workshops/search/", {"name": workshop_with_existing_email.name}
        )
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data) == 1
        assert response.data[0]["name"] == workshop_with_existing_email.name

    @pytest.mark.django_db
    def test_filter_workshop_by_account__username(
        self, client: APIClient, workshop_with_existing_email: Workshop
    ):

        response: Response = client.get(
            "/workshops/search/",
            {"account__username": workshop_with_existing_email.account.username},
        )
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data) == 1
        assert (
            response.data[0]["account"]["username"]
            == workshop_with_existing_email.account.username
        )

    @pytest.mark.django_db
    def test_filter_workshop_by_account__phone_number(
        self, client: APIClient, workshop_with_existing_email: Workshop
    ):
        response: Response = client.get(
            "/workshops/search/",
            {
                "account__phone_number": workshop_with_existing_email.account.phone_number
            },
        )
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data) == 1
        assert (
            response.data[0]["account"]["phone_number"]
            == workshop_with_existing_email.account.phone_number
        )

    @pytest.mark.django_db
    def test_filter_workshop_by_address(
        self, client: APIClient, workshop_with_existing_email: Workshop
    ):
        response: Response = client.get(
            "/workshops/search/", {"address": workshop_with_existing_email.address}
        )
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data) == 1
        assert response.data[0]["address"] == workshop_with_existing_email.address

    @pytest.mark.django_db
    def test_filter_workshop_by_services__name(
        self,
        client: APIClient,
        workshop_with_existing_email: Workshop,
    ):
        response: Response = client.get("/workshops/search/", {"services__name": "Oil"})
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data) == 1
        assert response.data[0]["services"][0]["name"] == "Oil"

    @pytest.mark.django_db
    def test_filter_workshop_by_price_range(
        self, client: APIClient, workshop_with_existing_email: Workshop
    ):
        min_price = 100
        max_price = 200
        response: Response = client.get(
            "/workshops/search/",
            {"services__price__gte": min_price, "services__price__lte": max_price},
        )
        assert response.status_code == status.HTTP_200_OK
        assert all(
            min_price <= workshop["services"][0]["price"] <= max_price
            for workshop in response.data
        )

    @pytest.mark.django_db
    def test_workshop_details_endpoint_returns_200(self, workshop_instance, client):
        response = client.get(f"/workshops/{workshop_instance.id}/")
        assert response.status_code == status.HTTP_200_OK

    @pytest.mark.django_db
    def test_workshop_details_endpoint_returns_expected_data(
        self, client, workshop_data, workshop_instance
    ):
        response = client.get(f"/workshops/{workshop_instance.id}/")
        response_data = response.json()
        workshop_data["account"].pop("password")
        assert response_data == workshop_data

    @pytest.mark.django_db
    def test_invalid_workshop_account_id_returns_404_workshop_not_found(self, client):
        response = client.get(f"/workshops/{5}/")
        response_data = response.json()
        assert response_data["message"] == "Workshop does not exist"
