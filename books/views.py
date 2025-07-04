from rest_framework import status
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import AllowAny
from rest_framework.decorators import action

from .serializers import BooksSerializer, PostBookSerializer
from .models import Books
from users.permissions import IsSuperAdmin


class BooksViewSet(ModelViewSet):
    queryset = Books.objects.all()
    serializer_class = BooksSerializer


    def get_permissions(self):

        if self.action in ("create", "destroy", "update", "partial_update"):
            return [IsSuperAdmin()]

        return [AllowAny()]


    def get_serializer_class(self):
        if self.action == "create":
            return PostBookSerializer

        return BooksSerializer


    def list(self, request, *args, **kwargs):
        book_title = request.query_params.get("title")

        if book_title:
            book = Books.objects.filter(title__iexact=book_title).first()

            if not book:
                return Response({"error": f"Book with name {book_title} not found"}, status=status.HTTP_404_NOT_FOUND)

            serializer = self.get_serializer(book)

            return Response(serializer.data, status=status.HTTP_200_OK)

        return super().list(request, *args, **kwargs)


    @action(detail=False, methods=["get"], url_path="(?P<name>[^/.]+)")
    def get_by_category(self, request, name=None):
        books = Books.objects.filter(category__name__iexact=name)
        serializer = self.get_serializer(books, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)

