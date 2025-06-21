from django.contrib.auth import authenticate
from rest_framework import status
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken

from .models import User
from .serializers import UserSerializer
from .permissions import IsSuperAdmin, IsSelfOrReadOnly


class UserViewSet(ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def get_permissions(self):

        if self.action in ("list", "create", "destroy"):
            return [IsSuperAdmin()]

        elif self.action in ("update", "partial_update"):
            return [IsSelfOrReadOnly()]

        return [IsAuthenticated()]



class UserRegistration(APIView):

    permission_classes = [AllowAny]

    def post(self, request):

        serializer = UserSerializer(data=request.data)

        if serializer.is_valid():
            user = serializer.save()

            refresh = RefreshToken.for_user(user)
            refresh.payload.update({
                "sub": user.id
            })

            return Response(
                {"refresh": str(refresh), "access": str(refresh.access_token)},
                status=status.HTTP_201_CREATED
            )


class UserLogin(APIView):

    permission_classes = [AllowAny]

    def post(self, request):

        data = request.data

        username = data.get("username", None)
        password = data.get("password", None)

        if username is None or password is None:
            return Response({"error": "Нужна ввести и логин, и пароль"}, status=status.HTTP_400_BAD_REQUEST)

        user = authenticate(username=username, password=password)

        if user is None:
            return Response({"error": "Введена неверные данные"}, status=status.HTTP_400_BAD_REQUEST)

        refresh = RefreshToken.for_user(user)
        refresh.payload.update({
            "sub": user.id
        })

        return Response({
            "refresh": str(refresh),
            "access": str(refresh.access_token)
        }, status=status.HTTP_200_OK)


class UserLogout(APIView):

    permission_classes = [IsAuthenticated]

    def post(self, request):

        refresh_token = request.data.get("refresh")

        if not refresh_token:
            return Response({'error': 'Необходим Refresh token'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            token = RefreshToken(refresh_token)
            token.blacklist()

        except Exception:
            return Response({'error': 'Неверный Refresh token'}, status=status.HTTP_400_BAD_REQUEST)

        return Response({'success': 'Выход успешен'}, status=status.HTTP_200_OK)

