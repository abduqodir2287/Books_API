import pytest
from rest_framework.test import APIClient
from rest_framework_simplejwt.tokens import RefreshToken

from users.models import User
from category.models import Category
from books.models import Books



@pytest.fixture
def superadmin_user(db):
    return User.objects.create_user(username="abduqodir", password="04042000", role="superadmin")


@pytest.fixture
def regular_user(db):
    return User.objects.create_user(username="saloh", password="shaxmatist", role="user")


@pytest.fixture
def superadmin_token(superadmin_user):
    refresh = RefreshToken.for_user(superadmin_user)
    return str(refresh.access_token)


@pytest.fixture
def regular_token(regular_user):
    refresh = RefreshToken.for_user(regular_user)
    return str(refresh.access_token)


@pytest.fixture
def auth_client_superadmin(superadmin_token):
    client = APIClient()
    client.credentials(HTTP_AUTHORIZATION=f"Bearer {superadmin_token}")
    return client


@pytest.fixture
def auth_client_user(regular_token):
    client = APIClient()
    client.credentials(HTTP_AUTHORIZATION=f"Bearer {regular_token}")
    return client


@pytest.fixture
def create_category(db):
    return Category.objects.create(name="Fantasy", description="Description for this category")


@pytest.fixture
def create_book(db, create_category):
    return Books.objects.create(
        title="Bolalik",
        author="Oybek",
        genre="Fantasy",
        language="Uzbek",
        category=create_category
    )

