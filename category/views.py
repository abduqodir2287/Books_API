from rest_framework.permissions import AllowAny
from rest_framework.viewsets import ModelViewSet

from users.permissions import IsSuperAdmin
from .serializers import CategorySerializer
from .models import Category


class CategoryViewSet(ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


    def get_permissions(self):

        if self.action in ("create", "destroy", "update", "partial_update"):
            return [IsSuperAdmin()]

        return [AllowAny()]
