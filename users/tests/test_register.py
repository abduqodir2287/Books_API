import pytest
from rest_framework.test import APIClient
from rest_framework import status


@pytest.mark.django_db
def test_register_success():
    data = {"username": "abduqodir", "password": "password", "email": "example@gmail.com"}
    client = APIClient()

    response = client.post("/users/user/register/", data)

    assert response.status_code == status.HTTP_201_CREATED
    assert "access" in response.data
    assert "refresh" in response.data


@pytest.mark.django_db
@pytest.mark.parametrize(
    "data",
    [
        ({"username": "abduqodir"}),
        ({"password": "password"}),
    ]
)
def test_register_fail(data: dict):
    client = APIClient()
    response = client.post("/users/user/register/", data)

    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert "access" not in response.data

