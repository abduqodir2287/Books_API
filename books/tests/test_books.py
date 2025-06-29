import pytest
from rest_framework import status
from rest_framework.test import APIClient


@pytest.mark.django_db
class TestBooksRouter:


    def test_get_books(self, create_book):
        client = APIClient()
        response = client.get("/books/")

        assert response.status_code == status.HTTP_200_OK
        assert "count" in response.data


    def test_get_book_by_title(self, create_book):
        client = APIClient()
        response = client.get(f"/books/?title={create_book.title}")

        assert response.status_code == status.HTTP_200_OK
        assert response.data["title"] == create_book.title


    def test_get_book_by_category(self, create_book):
        client = APIClient()
        response = client.get(f"/books/{create_book.category.name}/")

        assert response.status_code == status.HTTP_200_OK
        assert any(book["title"] == create_book.title for book in response.data)


    def test_add_book_superadmin(self, auth_client_superadmin, create_category):
        data = {
            "title": "Harry Potter", "author": "Abduqodiriy",
            "genre": "Fantasy", "language": "English", "category": create_category.id
        }
        response = auth_client_superadmin.post("/books/", data=data)

        assert response.status_code == status.HTTP_201_CREATED
        assert response.data["author"] == "Abduqodiriy"


    def test_add_book_user(self, auth_client_user, create_category):
        data = {
            "title": "Harry Potter", "author": "Abduqodiriy",
            "genre": "Fantasy", "language": "English", "category": create_category.id
        }
        response = auth_client_user.post("/books/", data=data)

        assert response.status_code == status.HTTP_403_FORBIDDEN


