import pytest
from rest_framework.test import APIClient
from rest_framework import status

from category.models import Category


@pytest.mark.django_db
class TestCategoryRouter:


    def test_get_category(self, create_category):
        client = APIClient()
        response = client.get("/category/")

        assert response.status_code == status.HTTP_200_OK
        assert "count" in response.data


    def test_get_category_by_id(self, create_category):
        client = APIClient()
        response = client.get(f"/category/{create_category.id}/")

        assert response.status_code == status.HTTP_200_OK
        assert response.data["name"] == create_category.name


    def test_add_category_superadmin(self, auth_client_superadmin):
        data = {"name": "Adventure", "description": "Жанр Приключения"}

        response = auth_client_superadmin.post("/category/", data=data)

        assert response.status_code == status.HTTP_201_CREATED
        assert response.data["name"] == "Adventure"


    def test_add_category_user(self, auth_client_user):
        data = {"name": "Adventure", "description": "Жанр Приключения"}

        response = auth_client_user.post("/category/", data=data)

        assert response.status_code == status.HTTP_403_FORBIDDEN


    def test_delete_category_superadmin(self, auth_client_superadmin, create_category):
        response = auth_client_superadmin.delete(f"/category/{create_category.id}/")

        assert response.status_code == status.HTTP_204_NO_CONTENT
        assert not Category.objects.filter(id=create_category.id).exists()


    def test_delete_category_user(self, auth_client_user, create_category):
        response = auth_client_user.delete(f"/category/{create_category.id}/")

        assert response.status_code == status.HTTP_403_FORBIDDEN


    def test_update_category_superadmin(self, auth_client_superadmin, create_category):
        response = auth_client_superadmin.patch(f"/category/{create_category.id}/", data={"name": "Science Fiction"})

        assert response.status_code == status.HTTP_200_OK
        assert response.data["name"] == "Science Fiction"


    def test_update_category_user(self, auth_client_user, create_category):
        response = auth_client_user.patch(f"/category/{create_category.id}/", data={"name": "Science Fiction"})

        assert response.status_code == status.HTTP_403_FORBIDDEN


