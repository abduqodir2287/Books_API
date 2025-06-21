from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView
from rest_framework.routers import DefaultRouter

from .views import UserViewSet, UserRegistration, UserLogin, UserLogout


router = DefaultRouter()
router.register(r"", UserViewSet, basename="users")


urlpatterns = router.urls + [
    path("user/register/", UserRegistration.as_view(), name="register"),
    path("user/login/", UserLogin.as_view(), name="login"),
    path("user/logout/", UserLogout.as_view(), name="logout"),
    path("user/token/refresh/", TokenRefreshView.as_view(), name="token-refresh")
]
