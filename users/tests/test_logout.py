import pytest
from rest_framework.test import APIClient
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework import status



@pytest.mark.django_db
class TestUserLogout:


    def test_logout_success(self, auth_client_user, regular_user):
        refresh = RefreshToken.for_user(regular_user)

        response = auth_client_user.post("/users/user/logout/", data={"refresh": str(refresh)})

        assert response.status_code == status.HTTP_200_OK
        assert response.data == {'success': 'Выход успешен'}


    def test_logout_without_refresh(self, auth_client_user):
        response = auth_client_user.post("/users/user/logout/", data={})

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response.data == {'error': 'Необходим Refresh token'}


    def test_logout_invalid_token(self, auth_client_user):
        response = auth_client_user.post("/users/user/logout/", data={"refresh": "data.not.valid"})

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response.data == {'error': 'Неверный Refresh token'}


    def test_logout_unauthorized(self):
        client = APIClient()
        response = client.post("/users/user/logout/", data={})

        assert response.status_code == status.HTTP_401_UNAUTHORIZED


