from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework import status

from .serializers import PostReviewSerializer, GetReviewSerializer
from .models import Review
from users.permissions import IsSelfOrSuperadmin
from .tasks import recalculate_book_rating


class ReviewViewSet(ModelViewSet):
    queryset = Review.objects.all()
    serializer_class = GetReviewSerializer
    permission_classes = [IsSelfOrSuperadmin]
    lookup_field = 'pk'


    def get_permissions(self):
        if self.action == "create":
            return [IsAuthenticated()]

        elif self.action in ("update", "partial_update", "destroy"):
            return [IsAuthenticated(), IsSelfOrSuperadmin()]

        return [AllowAny()]



    def create(self, request, *args, **kwargs):

        serializer = PostReviewSerializer(data=request.data)

        if serializer.is_valid():
            review = serializer.save(user=request.user)

            if review.rating:
                recalculate_book_rating.delay(review.book.id)

            return Response({"message": "Review created!"}, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


