from category.serializers import BooksCategorySerializer
from rest_framework.serializers import ModelSerializer

from .models import Books


class BooksSerializer(ModelSerializer):
    category = BooksCategorySerializer(read_only=True)

    class Meta:
        model = Books
        fields = "__all__"


class PostBookSerializer(ModelSerializer):

    class Meta:
        model = Books
        fields = "__all__"


class BookInfoSerializer(ModelSerializer):
    class Meta:
        model = Books
        fields = ["id", "title"]

