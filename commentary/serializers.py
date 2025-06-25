from rest_framework.serializers import ModelSerializer

from .models import Review
from users.serializers import UserInfoSerializer
from books.serializers import BookInfoSerializer


class PostReviewSerializer(ModelSerializer):

    class Meta:
        model = Review
        fields = ["id", "book", "text", "rating", "created_at", "updated_at"]


class GetReviewSerializer(ModelSerializer):
    book = BookInfoSerializer(read_only=True)
    user = UserInfoSerializer(read_only=True)

    class Meta:
        model = Review
        fields = ["id", "book", "user", "text", "rating", "created_at", "updated_at"]

