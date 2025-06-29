import pytest
from rest_framework import status
from rest_framework.test import APIClient

from users.models import User



@pytest.mark.django_db
class TestUsersRouter:


    def test_get_users_superadmin(self, auth_client_superadmin):
        response = auth_client_superadmin.get("/users/")

        assert response.status_code == status.HTTP_200_OK
        assert "count" in response.data


    def test_get_users_user(self, auth_client_user):
        response = auth_client_user.get("/users/")

        assert response.status_code == status.HTTP_403_FORBIDDEN


    def test_get_users_unauthorized(self):
        client = APIClient()
        response = client.get("/users/")

        assert response.status_code == status.HTTP_401_UNAUTHORIZED
        assert response.data == {"detail": "Authentication credentials were not provided."}


    def test_get_me_user(self, auth_client_user):
        response = auth_client_user.get("/users/me/")

        assert response.status_code == status.HTTP_200_OK


    def test_get_me_unauthorized(self):
        client = APIClient()
        response = client.get("/users/me/")

        assert response.status_code == status.HTTP_401_UNAUTHORIZED


    def test_get_user_by_id_user(self, auth_client_user, regular_user):
        response = auth_client_user.get(f"/users/{regular_user.id}/")

        assert response.status_code == status.HTTP_200_OK
        assert response.data["username"] == regular_user.username


    def test_get_user_by_id_unauthorized(self, regular_user):
        client = APIClient()
        response = client.get(f"/users/{regular_user.id}/")

        assert response.status_code == status.HTTP_401_UNAUTHORIZED


    def test_add_user_superadmin(self, auth_client_superadmin):
        response = auth_client_superadmin.post("/users/", data={"username": "user", "password": "password"})

        assert response.status_code == status.HTTP_201_CREATED


    def test_add_user_user(self, auth_client_user):
        response = auth_client_user.post("/users/", data={"username": "user", "password": "password"})

        assert response.status_code == status.HTTP_403_FORBIDDEN


    def test_add_user_unauthorized(self):
        client = APIClient()
        response = client.post("/users/", data={"username": "user", "password": "password"})

        assert response.status_code == status.HTTP_401_UNAUTHORIZED
        assert response.data == {"detail": "Authentication credentials were not provided."}


    def test_delete_user_superadmin(self, auth_client_superadmin):
        user = User.objects.create_user(username="user", password="password")

        response = auth_client_superadmin.delete(f"/users/{user.id}/")

        assert response.status_code == status.HTTP_204_NO_CONTENT
        assert User.objects.filter(id=user.id).count() == 0


    def test_delete_user_user(self, auth_client_user):
        user = User.objects.create_user(username="user", password="password")

        response = auth_client_user.delete(f"/users/{user.id}/")

        assert response.status_code == status.HTTP_403_FORBIDDEN


    def test_delete_user_unauthorized(self):
        user = User.objects.create_user(username="user", password="password")
        client = APIClient()

        response = client.delete(f"/users/{user.id}/")

        assert response.status_code == status.HTTP_401_UNAUTHORIZED


    def test_user_self_update(self, auth_client_user, regular_user):
        response = auth_client_user.patch("/users/me/", data={"first_name": "Hello"})
        regular_user.refresh_from_db()

        assert response.status_code == status.HTTP_200_OK
        assert regular_user.first_name == "Hello"


    def test_user_update_unauthorized(self):
        client = APIClient()
        response = client.patch("/users/me/", data={"first_name": "Hello"})

        assert response.status_code == status.HTTP_401_UNAUTHORIZED



