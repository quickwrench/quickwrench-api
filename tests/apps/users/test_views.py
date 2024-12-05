import pytest
from rest_framework import status


class TestRegister:
    @pytest.mark.django_db
    def test_register_success_201(self, client, user_data):
        response = client.post("/accounts/register/", user_data, format="json")
        assert response.status_code == status.HTTP_201_CREATED
        assert response.data["username"] == user_data["username"]
        assert response.data["email"] == user_data["email"]

    @pytest.mark.django_db
    def test_register_with_existing_email(
        self, client, user_data, user_with_existing_email
    ):
        user_data["email"] = user_with_existing_email.email
        response = client.post("/accounts/register/", user_data, format="json")
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert "email" in response.data
        assert response.data["email"] == ["An account with this email already exists."]
