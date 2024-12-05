import pytest
from rest_framework import status


class TestRegister:
    @pytest.mark.django_db
    def test_register_success_201(self, client, user_data):
        response = client.post("/users/register/", user_data, format="json")
        assert response.status_code == status.HTTP_201_CREATED
        assert response.data["account"]["username"] == user_data["account"]["username"]
        assert response.data["account"]["email"] == user_data["account"]["email"]
        assert response.data["first_name"] == user_data["first_name"]
        assert response.data["last_name"] == user_data["last_name"]
        assert response.data["car_make"] == user_data["car_make"]

    @pytest.mark.django_db
    def test_register_with_existing_email(self, client, user_with_existing_email):
        payload = {
            "account": {
                "email": user_with_existing_email.account.email,
                "username": "newuser",
                "password": "newpassword",
            },
            "first_name": "Jane",
            "last_name": "Doe",
            "car_make": "Toyota",
        }

        response = client.post("/users/register/", payload, format="json")

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert "email" in response.data["account"]
        assert response.data["account"]["email"] == [
            "account with this email already exists."
        ]

    @pytest.mark.django_db
    @pytest.mark.parametrize(
        "invalid_email",
        [
            "invalidemail.com",
            "@missingusername.com",
            "test@.com",
        ],
    )
    def test_register_with_invalid_email(self, client, user_data, invalid_email):
        user_data["account"]["email"] = invalid_email
        response = client.post("/users/register/", user_data, format="json")
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert "email" in response.data["account"]

    @pytest.mark.django_db
    def test_register_missing_username(self, client, user_data):
        user_data["account"]["username"] = ""
        response = client.post("/users/register/", user_data, format="json")
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert "username" in response.data["account"]
        assert response.data["account"]["username"] == ["This field may not be blank."]

    @pytest.mark.django_db
    def test_register_missing_password(self, client, user_data):
        user_data["account"]["password"] = ""
        response = client.post("/users/register/", user_data, format="json")
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert "password" in response.data["account"]
        assert response.data["account"]["password"] == ["This field may not be blank."]
