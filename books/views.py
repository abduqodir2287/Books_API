from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import AllowAny

from .serializers import BooksSerializers
from .models import Books
from users.permissions import IsSuperAdmin


class BooksViewSet(ModelViewSet):
    queryset = Books.objects.all()
    serializer_class = BooksSerializers


    def get_permissions(self):

        if self.action in ("create", "destroy", "update", "partial_update"):
            return [IsSuperAdmin()]

        return [AllowAny()]
