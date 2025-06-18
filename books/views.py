from rest_framework.viewsets import ModelViewSet

from .serializers import BooksSerializers
from .models import Books


class BooksViewSet(ModelViewSet):
    queryset = Books.objects.all()
    serializer_class = BooksSerializers
