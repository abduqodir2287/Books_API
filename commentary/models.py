from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator

from users.models import User
from books.models import Books



class Review(models.Model):
    book = models.ForeignKey(Books, on_delete=models.CASCADE, related_name="reviews")
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="reviews")
    text = models.TextField()
    rating = models.PositiveSmallIntegerField(
        null=True, blank=True,
        validators=[
            MinValueValidator(1),
            MaxValueValidator(5)
        ])
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


    def __str__(self) -> str:
        return f"Review by {self.user.username} on {self.book.title}"

