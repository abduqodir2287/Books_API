import pytest
from rest_framework import status
from rest_framework.test import APIClient

from users.models import User


@pytest.mark.django_db
def test_login_success():
    user = User.objects.create_user(username="user", password="password")
    client = APIClient()
    response = client.post("/users/user/login/", {"username": "user", "password": "password"})

    assert response.status_code == status.HTTP_200_OK
    assert "access" in response.data
    assert "refresh" in response.data


@pytest.mark.django_db
def test_login_invalid():
    client = APIClient()
    response = client.post("/users/user/login/", {"username": "wrong", "password": "wrong"})

    assert response.status_code == status.HTTP_400_BAD_REQUEST or response.status_code == status.HTTP_401_UNAUTHORIZED


