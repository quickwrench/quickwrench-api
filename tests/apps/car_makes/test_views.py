import pytest
from rest_framework import status


class TestCarMake:

    @pytest.mark.django_db
    def test_carmake_returns_instance_200(self, client, load_data):
        response = client.get("/carmakes/")
        data = response.json()
        instance_count = len(data)
        print(data)
        assert response.status_code == status.HTTP_200_OK
        assert instance_count == 5
